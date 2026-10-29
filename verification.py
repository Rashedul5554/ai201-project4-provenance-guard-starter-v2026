"""Local reviewer-issued creator credential. No automatic human detection.

A reviewer must observe the live challenge before approving it. Tokens and
challenge state stay in .private/ and must never be committed.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import time
import uuid

import config

PRIVATE = config.ROOT / ".private"
STATE = PRIVATE / "verification.json"
WRITER = PRIVATE / "writer_credential.json"


def _read():
    if not STATE.exists():
        return {"requests": {}, "credentials": {}}
    return json.loads(STATE.read_text(encoding="utf-8"))


def _write(state):
    PRIVATE.mkdir(mode=0o700, parents=True, exist_ok=True)
    temporary = PRIVATE / ("state-" + secrets.token_hex(8) + ".tmp")
    temporary.write_text(json.dumps(state, indent=2), encoding="utf-8")
    temporary.chmod(0o600)
    os.replace(temporary, STATE)


def create_request(creator_id):
    if not isinstance(creator_id, str) or not creator_id.strip():
        raise ValueError("creator_id must be a non-empty string.")
    state = _read()
    rid = str(uuid.uuid4())
    phrase = " ".join(secrets.choice(["river", "copper", "window", "orchid", "lantern", "harbor", "violet", "sparrow"]) for _ in range(6))
    item = {"request_id": rid, "creator_id": creator_id.strip(),
            "challenge": phrase, "created_at": time.time(), "approved": False}
    state["requests"][rid] = item
    state["latest_request"] = rid
    _write(state)
    return item


def approve(request_id, reviewer, observed=False):
    if not observed or not isinstance(reviewer, str) or not reviewer.strip():
        raise ValueError("A named reviewer must confirm observing the live task.")
    state = _read()
    if request_id == "latest":
        request_id = state.get("latest_request")
    item = state["requests"].get(request_id)
    if item is None or item["approved"]:
        raise ValueError("Request is unknown or already approved.")
    if time.time() - item["created_at"] > 1800:
        raise ValueError("Challenge expired after 30 minutes. Request another.")
    token = secrets.token_urlsafe(32)
    credential = {"credential_id": str(uuid.uuid4()),
                  "creator_id": item["creator_id"], "reviewer": reviewer.strip(),
                  "issued_at": time.time(),
                  "badge": "Verified human — local reviewer check",
                  "scope": "Creator completed an observed task; authorship of later items is not verified."}
    state["credentials"][hashlib.sha256(token.encode()).hexdigest()] = credential
    item["approved"] = True
    _write(state)
    WRITER.write_text(json.dumps({"token": token, "creator_id": item["creator_id"]}), encoding="utf-8")
    WRITER.chmod(0o600)
    return credential


def credential_for(creator_id, token):
    if not isinstance(token, str) or not token:
        return None
    digest = hashlib.sha256(token.encode()).hexdigest()
    credential = _read()["credentials"].get(digest)
    if credential and credential["creator_id"] == creator_id:
        return dict(credential)
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    req = commands.add_parser("request")
    req.add_argument("--creator", required=True)
    approve_parser = commands.add_parser("approve")
    approve_parser.add_argument("--request", default="latest")
    approve_parser.add_argument("--reviewer", required=True)
    args = parser.parse_args()
    try:
        if args.command == "request":
            print(json.dumps(create_request(args.creator), indent=2))
            print("Reviewer: observe the writer read the phrase and compose a short original paragraph live.")
        else:
            print("Approve only after personally observing the creator read the challenge and write a paragraph live.")
            observed = input("Reviewer: type OBSERVED to confirm (anything else cancels): ") == "OBSERVED"
            print(json.dumps(approve(args.request, args.reviewer, observed), indent=2))
            print("Private token saved in .private/writer_credential.json. Do not share or commit it.")
    except ValueError as error:
        parser.exit(1, str(error) + "\n")
