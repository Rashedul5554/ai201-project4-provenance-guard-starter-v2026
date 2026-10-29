"""Capture real local-service evidence and fill the Unit 7 README.

Run after a reviewer completes the observed verification task. This script
never approves credentials automatically and never writes secret tokens to evidence.
"""
from pathlib import Path
import json
import requests
import verification

BASE = "http://127.0.0.1:5000"
events = []


def call(method, path, payload=None, expected=200):
    response = requests.request(method, BASE + path, json=payload, timeout=180)
    body = response.json()
    public_payload = None if payload is None else {
        k: ("<private creator-bound token supplied locally>" if k == "verification_token" else v)
        for k, v in payload.items()
    }
    events.append({"method": method, "path": path, "request": public_payload,
                   "http_status": response.status_code, "response": body})
    if response.status_code != expected:
        raise RuntimeError(f"{method} {path}: expected {expected}, received {response.status_code}: {body}")
    return body


def block(value):
    return "```json\n" + json.dumps(value, indent=2, ensure_ascii=False) + "\n```\n"


def replace_between(text, start, end, content):
    left, rest = text.split(start, 1)
    _, right = rest.split(end, 1)
    return left + start + "\n" + content + "\n" + end + right


def main():
    if not verification.WRITER.exists():
        raise SystemExit("Complete the live reviewer challenge first; see BONUS_STEPS.md.")
    writer = json.loads(verification.WRITER.read_text(encoding="utf-8"))
    credential = verification.credential_for(writer["creator_id"], writer["token"])
    if credential is None:
        raise SystemExit("Local creator credential could not be validated.")

    p1 = "I checked the school laptop and recorded the fault."
    p2 = p1 + " The wireless adapter was disabled after an update."
    p3 = p2 + " I enabled the adapter and tested the connection again."
    drafts = [p1, p2, p3]
    payload = {"text": p3, "creator_id": writer["creator_id"],
               "draft_history": drafts, "verification_token": writer["token"]}
    decision = call("POST", "/submit", payload)
    assert decision["provenance_score"] == 0.2, "Third signal is not connected."
    expected_score = round(.4 * decision["model_score"] + .4 * decision["style_score"] + .2 * .2, 4)
    assert abs(decision["combined_score"] - expected_score) < .00001
    assert decision["human_credential"]["credential_id"] == credential["credential_id"]
    cid = decision["content_id"]
    before = call("GET", "/content/" + cid)
    assert before["status"] == "decided"
    appeal = call("POST", "/appeal", {"content_id": cid, "reasoning": "Please review this diagnostic submission. The example draft text was supplied by AI; the creator credential is not proof of this item's authorship."})
    after = call("GET", "/content/" + cid)
    assert appeal["status"] == after["status"] == "under_review"
    assert after["human_credential"]["credential_id"] == credential["credential_id"]
    call("GET", "/content/no-such-id", expected=404)
    call("POST", "/submit", {"text": p3, "creator_id": writer["creator_id"] + "-other", "verification_token": writer["token"]}, expected=403)
    no_draft = call("POST", "/submit", {"text": p3, "creator_id": "bonus-no-draft"})
    assert no_draft["provenance_score"] == 0.5

    diagnostic = ("Rain stopped. Beneath the viaduct, a watchmaker in saffron boots wrestled a buckled accordion case past the fishmonger's shutter, scattering receipts, brass washers, and a single bruised persimmon across the cobbles while a tram screeched somewhere uphill. Nobody claimed the fruit.")
    repetitive = " ".join(["The system is designed to provide clear and consistent results."] * 8)
    candidates = [("ai-unusual-diagnostic", diagnostic), ("ai-repetitive-diagnostic", repetitive)]
    for filename in ["human_personal.txt", "human_formal.txt"]:
        if Path(filename).exists():
            candidates.append((filename, Path(filename).read_text(encoding="utf-8")))
    labels = {decision["guess"], no_draft["guess"]}
    for name, text in candidates:
        r = call("POST", "/submit", {"text": text, "creator_id": name})
        labels.add(r["guess"])
    matching = [e for e in call("GET", "/log")["entries"] if e.get("content_id") == cid]
    assert matching[0]["status"] == "decided" and matching[-1]["status"] == "under_review"
    assert writer["token"] not in json.dumps(events)
    evidence = {"note": "Real local-service responses. Diagnostic paragraphs and drafts are AI-generated. Human verification was a separate reviewer-observed task; scoring does not establish authorship.",
                "labels_observed": sorted(labels), "events": events, "matching_log_entries": matching}
    Path("results").mkdir(exist_ok=True)
    Path("results/bonus_evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False), encoding="utf-8")
    readme_path = Path("README.md")
    readme = readme_path.read_text(encoding="utf-8")
    sample = ("Actual three-signal submission and appeal, followed by content lookup. "
              "The credential token is omitted from published evidence. "
              "Requests were sent by `capture_bonus_evidence.py` using Python requests.\n\n")
    for item in events[:4]:
        sample += f"**{item['method']} {item['path']} — HTTP {item['http_status']}**\n\n" + block(item)
    sample += "**Matching audit entries (original decision and appeal)**\n\n" + block(matching)
    readme = replace_between(readme, "<!-- BONUS_SAMPLE_START -->", "<!-- BONUS_SAMPLE_END -->", sample)
    extra = ("Actual local results are saved in `results/bonus_evidence.json`.\n\n"
             f"Labels observed under the new weights: {', '.join(sorted(labels))}.\n\n"
             "The sample above shows a provenance score of 0.20, a creator credential on an item, and lookup moving from decided to under_review. Missing-history input returned 0.50. Unknown content returned 404; a token used with another creator returned 403.\n\n"
             "Diagnostic texts were supplied by AI and were not the reviewer's live writing task. The badge does not attest to their authorship.\n\n")
    extra += block({"creator_credential": decision["human_credential"],
                    "lookup_before_appeal": before, "lookup_after_appeal": after,
                    "diagnostic_requests_and_responses": events[4:-1]})
    if labels != {"human", "unsure", "ai"}:
        extra += "\n**Label coverage still needs attention: missing " + str(sorted({"human", "unsure", "ai"} - labels)) + ". Do not claim all labels were observed in this run.**\n"
    readme = replace_between(readme, "<!-- BONUS_EVIDENCE_START -->", "<!-- BONUS_EVIDENCE_END -->", extra)
    readme_path.write_text(readme, encoding="utf-8")
    print("Saved results/bonus_evidence.json and updated README with real evidence.")
    print("Labels observed:", sorted(labels))
    print("Third signal, credential, status lookup before/after appeal, and negative checks passed.")


if __name__ == "__main__":
    main()
