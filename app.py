#!/usr/bin/env python3
"""Provenance Guard — the web service."""

import uuid

from flask import Flask, jsonify, request

import audit
import config
import detector
import scoring
import stylometry
import provenance
import verification

app = Flask(__name__)


# Rate limiting — Unit 8. Disabled until enabled in config.py.
class _LimiterOff:
    """Keep limit decorators harmless while rate limiting is disabled."""

    def limit(self, *args, **kwargs):
        return lambda view: view


limiter = _LimiterOff()

if config.RATE_LIMITING_ENABLED:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address

    def rate_limit_key():
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            return get_remote_address()

        creator = payload.get("creator_id")

        if isinstance(creator, str) and creator.strip():
            return creator

        return get_remote_address()

    limiter = Limiter(
        key_func=rate_limit_key,
        app=app,
        storage_uri=config.RATE_LIMIT_STORAGE,
        default_limits=[],
    )

    @app.errorhandler(429)
    def rate_limited(exc):
        payload = request.get_json(silent=True)

        if not isinstance(payload, dict):
            payload = {}

        audit.log_rejection(
            creator_id=payload.get("creator_id", "unknown"),
            reason="rate_limited",
            limit=str(exc.description),
        )

        return jsonify({
            "error": "rate_limited",
            "message": "Too many submissions. Try again shortly.",
            "limit": str(exc.description),
        }), 429


# The starter's control route. Keep unchanged.
@app.post("/ping")
def ping():
    payload = request.get_json(silent=True) or {}
    return jsonify({
        "ok": True,
        "you_sent": payload.get("message"),
        "service": "provenance-guard",
    })


@app.get("/health")
def health():
    """Report service health and whether the detector is loaded."""
    import detector

    loaded = detector._model is not None

    return jsonify({
        "ok": True,
        "detector_model": config.DETECTOR_MODEL,
        "detector_loaded": loaded,
        "rate_limiting": config.RATE_LIMITING_ENABLED,
        "log_entries": len(audit.read_entries()),
    })


@app.post("/submit")
# @limiter.limit(f"{config.RATE_LIMIT_PER_MINUTE}/minute;{config.RATE_LIMIT_PER_DAY}/day")
def submit():
    """Validate input, run both signals, return a label, and log the decision."""
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_input",
            "message": "Send a JSON object with text and creator_id.",
        }), 400

    text = payload.get("text")
    creator_id = payload.get("creator_id")

    if not isinstance(text, str) or not text.strip():
        return jsonify({
            "error": "invalid_input",
            "message": "text must be a non-empty string.",
        }), 400

    if not isinstance(creator_id, str) or not creator_id.strip():
        return jsonify({
            "error": "invalid_input",
            "message": "creator_id must be a non-empty string.",
        }), 400

    try:
        model_score = detector.model_signal(text)
    except detector.DetectorUnavailable:
        app.logger.exception("Detector could not be loaded")
        return jsonify({
            "error": "detector_unavailable",
            "message": "The detector could not load. Check the server terminal.",
        }), 503
    except ValueError:
        return jsonify({
            "error": "unscorable_text",
            "message": "Text could not be scored. Try a few complete sentences.",
        }), 400

    try:
        draft_score = provenance.draft_signal(text, payload.get("draft_history"))
    except ValueError as exc:
        return jsonify({"error": "invalid_input", "message": str(exc)}), 400
    credential = None
    if "verification_token" in payload:
        credential = verification.credential_for(creator_id.strip(), payload["verification_token"])
        if credential is None:
            return jsonify({"error": "invalid_credential", "message": "Credential token is invalid for this creator."}), 403

    style_score = stylometry.style_signal(text)
    combined_score = scoring.combine_signals(model_score, style_score, draft_score)
    content_id = str(uuid.uuid4())

    guess, label = scoring.score_to_label(combined_score)
    # Heuristic strength of the human/AI direction, not a calibrated probability.
    confidence = round(max(combined_score, 1.0 - combined_score), 4)

    audit.log_decision(
        content_id=content_id,
        creator_id=creator_id.strip(),
        guess=guess,
        model_score=model_score,
        style_score=style_score,
        combined_score=combined_score,
        label=label,
        status="decided",
        provenance_score=draft_score,
        human_credential=credential,
    )

    return jsonify({
        "content_id": content_id,
        "guess": guess,
        "confidence": confidence,
        "label": label,
        "model_score": model_score,
        "style_score": style_score,
        "combined_score": combined_score,
        "status": "decided",
        "provenance_score": draft_score,
        "human_credential": credential,
    }), 200

@app.post("/appeal")
def appeal():
    """Record an appeal; the latest log entry becomes the item's status."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({
            "error": "invalid_input",
            "message": "Send a JSON object with content_id and reasoning.",
        }), 400

    content_id = payload.get("content_id")
    reasoning = payload.get("reasoning")
    if not isinstance(content_id, str) or not content_id.strip():
        return jsonify({
            "error": "invalid_input",
            "message": "content_id must be a non-empty string.",
        }), 400
    if not isinstance(reasoning, str) or not reasoning.strip():
        return jsonify({
            "error": "invalid_input",
            "message": "reasoning must be a non-empty string.",
        }), 400

    content_id = content_id.strip()
    entries = audit.entries_for(content_id)
    original = next(
        (entry for entry in entries
         if entry.get("status") == "decided" and entry.get("event") != "appeal"),
        None,
    )
    if original is None:
        return jsonify({
            "error": "not_found",
            "message": "No completed submission was found for this content_id.",
        }), 404

    entry = audit.log_appeal(
        content_id=content_id,
        creator_id=original["creator_id"],
        reasoning=reasoning,
    )
    return jsonify({
        "content_id": content_id,
        "status": entry["status"],
        "message": "Your appeal has been recorded for review.",
    }), 200


@app.get("/content/<content_id>")
def get_content(content_id):
    """Return the original decision with the item's latest status."""
    entries = audit.entries_for(content_id)
    original = next((e for e in entries if e.get("status") == "decided"), None)
    if original is None:
        return jsonify({"error": "not_found", "message": "Content not found."}), 404
    current = dict(original)
    current["status"] = entries[-1]["status"]
    current["last_updated"] = entries[-1]["timestamp"]
    # Do not expose the appeal explanation or any credential secret here.
    return jsonify(current), 200


@app.get("/log")
def get_log():
    """Return audit entries, most recent last."""
    limit = request.args.get("limit", type=int)
    entries = audit.read_entries(limit=limit)

    return jsonify({
        "count": len(entries),
        "entries": entries,
    })


def main():
    print(f"Provenance Guard on http://{config.HOST}:{config.PORT}")
    print(f"  detector model:  {config.DETECTOR_MODEL}")
    print(
        f"  rate limiting:   "
        f"{'ON' if config.RATE_LIMITING_ENABLED else 'off (unit 8)'}"
    )
    print(f"  audit log:       {config.AUDIT_LOG}")
    print()
    print("Check it's alive:")
    print(f'  curl -X POST http://{config.HOST}:{config.PORT}/ping \\')
    print('    -H "Content-Type: application/json" \\')
    print("    -d '{\"message\": \"hello\"}'")
    print()

    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
    )


if __name__ == "__main__":
    main()
    
