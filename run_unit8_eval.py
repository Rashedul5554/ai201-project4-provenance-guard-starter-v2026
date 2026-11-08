"""Run the five original Unit 8 criteria without changing the service."""
import argparse
import hashlib
import json
import re
import time
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import uuid4

import requests

ROOT = Path(__file__).resolve().parent
BASE = "http://127.0.0.1:5000"
TARGETS = [
    ("Wrong AI accusations", "At most 1 of 10 human passages labeled ai"),
    ("Mean score separation", "AI mean minus human mean >= 0.15 over five matched pairs"),
    ("Label mapping", "All grid and boundary cases match documented labels; all three appear"),
    ("Appeals", "5 of 5 reach under_review, log reasoning and retain decision"),
    ("Invalid input", "6 of 6 return 400 with field error, no scored decision; ping returns 200"),
]


def load_data(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    human, pairs = data["human"], data["ai_pairs"]
    if len(human) != 10 or len(pairs) != 5:
        raise ValueError("Provide exactly ten human passages and five AI pairs.")
    missing = [row["id"] for row in human if not row["text"].strip()]
    missing += [row["id"] for row in pairs if not row["text"].strip() or not row["source"].strip()]
    if missing:
        raise ValueError("Fill in text (and AI source) for: " + ", ".join(missing))
    authors = {row["id"]: row for row in human}
    if len(authors) != 10 or len({row["text"].strip() for row in human}) != 10:
        raise ValueError("Use ten distinct human sample IDs and passages.")
    if sum(row["style"] in {"plain", "formal"} for row in human) < 3:
        raise ValueError("Mark at least three actual plain or formal passages.")
    matched = {row["human_id"] for row in pairs}
    if len(matched) != 5 or not matched <= authors.keys():
        raise ValueError("Each AI sample must match a different known human sample.")
    if len({row["id"] for row in pairs}) != 5 or len({row["text"].strip() for row in pairs}) != 5:
        raise ValueError("Use five distinct AI sample IDs and passages.")
    for row in pairs:
        other = authors[row["human_id"]]
        n = len(other["text"].split())
        m = len(row["text"].split())
        if abs(m - n) * 5 > n:
            raise ValueError(f"{row['id']} has {m} words; {other['id']} has {n}. Match within 20%.")
    return human, pairs


def call(method, path, payload=None):
    r = requests.request(method, BASE + path, json=payload, timeout=120)
    try:
        body = r.json()
    except ValueError:
        body = {"non_json": r.text[:300]}
    return {"http": r.status_code, "body": body if isinstance(body, dict) else {"unexpected_json": body}}


def log():
    r = call("GET", "/log")
    if r["http"] != 200 or not isinstance(r["body"].get("entries"), list):
        raise RuntimeError("Could not read the audit log.")
    return r["body"]["entries"]


def label_checks():
    import scoring

    doc = (ROOT / "README.md").read_text(encoding="utf-8").split("## Label Variants", 1)[1].split("## Sample Run", 1)[0]
    labels = dict(re.findall(r'\x60guess: (human|unsure|ai)\x60\).*?\n\s+Exact text: "([^"\n]+)"', doc))
    if set(labels) != {"human", "unsure", "ai"}:
        raise ValueError("Could not parse the three documented label sentences in README.md.")
    low = Decimal(re.search(r'0 <= score <= ([\d.]+)\x60', doc).group(1))
    high = Decimal(re.search(r'\x60([\d.]+) <= score <= 1\x60', doc).group(1))
    middle = re.search(r'\x60([\d.]+) < score < ([\d.]+)\x60', doc)
    if not middle or tuple(map(Decimal, middle.groups())) != (low, high) or not 0 <= low < high <= 1:
        raise ValueError("README label intervals are inconsistent.")
    scores = {Decimal(i) / 100 for i in range(101)}
    # Probe both documented boundaries and the running configuration's boundaries.
    for boundary in (low, high, Decimal(str(scoring.config.HUMAN_THRESHOLD)),
                     Decimal(str(scoring.config.AI_THRESHOLD))):
        scores.update(boundary + d for d in (Decimal("-0.000001"), Decimal(0), Decimal("0.000001")))
    rows = []
    for score in sorted(x for x in scores if 0 <= x <= 1):
        expected = "human" if score <= low else "ai" if score >= high else "unsure"
        guess, label = scoring.score_to_label(float(score))
        rows.append({"score": str(score), "expected": expected, "guess": guess,
                     "label": label, "ok": (guess, label) == (expected, labels[expected])})
    passed = sum(r["ok"] for r in rows)
    return result(passed == len(rows) and {r["guess"] for r in rows} == set(labels),
                  f"{passed}/{len(rows)} label checks", rows, "scoring.py::score_to_label")


def result(ok, measure, evidence, producer):
    return {"passed": ok, "measure": measure, "producer": producer, "evidence": evidence}


def run_trial(human, pairs, prefix):
    def submit(row, tag):
        return {"sample_id": row["id"], **call("POST", "/submit",
                {"text": row["text"], "creator_id": prefix + "-" + tag})}

    hr = {row["id"]: submit(row, f"h{i}") for i, row in enumerate(human)}
    ar = [submit(row, f"a{i}") for i, row in enumerate(pairs)]

    def scored(r):
        return r["http"] == 200 and isinstance(r["body"].get("combined_score"), (int, float)) and r["body"].get("guess") in {"ai", "human", "unsure"}

    false_ai = sum(r["body"].get("guess") == "ai" for r in hr.values())
    complete = all(map(scored, hr.values()))
    first = result(complete and false_ai <= 1, f"{false_ai}/10 labeled ai" + ("" if complete else "; incomplete scoring"),
                   list(hr.values()), "app.py::submit")
    matched = [hr[row["human_id"]] for row in pairs]
    gap = None
    if all(map(scored, matched + ar)):
        def mean(rs):
            return sum(Decimal(str(r["body"]["combined_score"])) for r in rs) / len(rs)
        gap = mean(ar) - mean(matched)
    second = result(gap is not None and gap >= Decimal("0.15"),
                    f"mean gap {gap}" if gap is not None else "incomplete scoring",
                    {"pairs": [{"human_id": row["human_id"], "ai_id": row["id"], "source": row["source"]} for row in pairs],
                     "human": matched, "ai": ar}, "app.py::submit and run_unit8_eval.py::run_trial")
    third = label_checks()

    appeals = []
    for i, row in enumerate(human[:5]):
        submitted = submit(row, f"appeal{i}")
        cid = submitted["body"].get("content_id")
        check = {"submission": submitted, "ok": False}
        if submitted["http"] == 200 and cid:
            reason = f"Unit 8 evaluation trial {prefix}: please review this decision."
            pre = [e for e in log() if e.get("content_id") == cid]
            request = {"content_id": cid, "reasoning": reason}
            response = call("POST", "/appeal", request)
            post = [e for e in log() if e.get("content_id") == cid]
            ok = (response["http"] == 200 and response["body"].get("content_id") == cid
                  and response["body"].get("status") == "under_review"
                  and any(e.get("status") == "decided" for e in pre)
                  and post[:len(pre)] == pre and len(post) == len(pre) + 1
                  and post[-1].get("event") == "appeal"
                  and post[-1].get("status") == "under_review"
                  and post[-1].get("reasoning") == reason)
            check.update(ok=ok, request=request, response=response, matching_log=post)
        appeals.append(check)
    n = sum(row["ok"] for row in appeals)
    fourth = result(n == 5, f"{n}/5 appeals", appeals, "app.py::submit, appeal, get_log")

    cases = [
        ("text", {"creator_id": prefix + "-bad0"}),
        ("text", {"creator_id": prefix + "-bad1", "text": ""}),
        ("text", {"creator_id": prefix + "-bad2", "text": "   "}),
        ("text", {"creator_id": prefix + "-bad3", "text": 42}),
        ("creator_id", {"text": human[0]["text"]}),
        ("creator_id", {"text": human[0]["text"], "creator_id": ""}),
    ]
    invalid = []
    for field, payload in cases:
        before = log()
        response = call("POST", "/submit", payload)
        after = log()
        new = after[len(before):]
        body = response["body"]
        ok = (response["http"] == 400 and bool(body.get("error"))
              and field in str(body.get("message", ""))
              and body.get("content_id") is None and body.get("guess") is None
              and after[:len(before)] == before
              and not any(e.get("status") == "decided" for e in new))
        invalid.append({"expected_field": field, "response": response, "new_log_entries": new, "ok": ok})
    ping = call("POST", "/ping", {"message": "unit8-eval"})
    n = sum(row["ok"] for row in invalid)
    fifth = result(n == 6 and ping["http"] == 200,
                   f"{n}/6 invalid cases; ping {ping['http']}",
                   {"cases": invalid, "ping": ping}, "app.py::submit, get_log, ping")
    return [first, second, third, fourth, fifth]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "unit8_samples.json")
    parser.add_argument("--label", default="before", choices=["before", "after", "after_second"])
    parser.add_argument("--check-data", action="store_true")
    args = parser.parse_args()
    try:
        human, pairs = load_data(args.data)
    except (OSError, KeyError, TypeError, ValueError) as e:
        parser.exit(2, f"Sample check failed: {e}\n")
    print("Sample checks passed: 10 human passages and 5 length-matched AI passages.")
    if args.check_data:
        return
    print("Run against your local app. Avoid other requests during the evaluation.")
    health = call("GET", "/health")
    if health["http"] != 200 or not health["body"].get("rate_limiting"):
        parser.exit(2, "Start the instrumented local service with rate limiting enabled.\n")
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    run_id = "unit8-" + uuid4().hex[:10]
    trials = []
    for i in range(1, 4):
        if i > 1:
            # Missing or blank creator IDs share an IP quota across trials.
            print("Waiting 61 seconds for the address quota to reset.", flush=True)
            time.sleep(61)
        print(f"Trial {i}/3", flush=True)
        trials.append(run_trial(human, pairs, f"{run_id}-{i}"))
    out = ROOT / "results"
    out.mkdir(exist_ok=True)
    name = f"criteria_{stamp}_{args.label}"
    digest = hashlib.sha256(args.data.read_bytes()).hexdigest()
    evidence = {"run_id": run_id, "label": args.label, "sample_sha256": digest, "trials": trials}
    (out / (name + ".json")).write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    lines = [f"# Unit 8 criteria — {args.label}", "", f"Dataset SHA-256: `{digest}`.", "",
             "| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |",
             "|---|---|---|---|---|---|"]
    for i, (title, target) in enumerate(TARGETS):
        rows = [trial[i] for trial in trials]
        verdict = "MET" if all(row["passed"] for row in rows) else "MISSED"
        lines.append(f"| {i+1}. {title} | {target} | " + " | ".join(r["measure"] for r in rows) + f" | {verdict} |")
    lines += ["", f"Full observed evidence (all trials): [{name}.json]({name}.json).",
              "Review the outcomes and diagnose each miss in your own words.", ""]
    (out / (name + ".md")).write_text("\n".join(lines))
    print(f"Saved results/{name}.md and .json")


if __name__ == "__main__":
    main()
