"""Measure the local GPT-2 service for the Unit 9 stretch evidence."""

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from time import perf_counter, sleep
from unittest.mock import patch

import requests


TEXT = (
    "I inspected the laptop after the update. The wireless adapter was disabled, "
    "so I enabled it and confirmed the device could connect again."
)
PORT = 19509
URL = f"http://127.0.0.1:{PORT}"
ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def running_server():
    env = dict(os.environ, HOST="127.0.0.1", PORT=str(PORT), AI201_DEBUG="0")
    with tempfile.TemporaryFile(mode="w+") as output:
        started = perf_counter()
        process = subprocess.Popen(
            [sys.executable, "app.py"], cwd=ROOT, env=env, stdout=output, stderr=output
        )
        try:
            while process.poll() is None and perf_counter() - started < 45:
                try:
                    ping = requests.post(f"{URL}/ping", json={"message": "hello"}, timeout=1)
                    if ping.ok and ping.json().get("ok") is True:
                        break
                except requests.ConnectionError:
                    sleep(0.05)
            else:
                output.seek(0)
                raise RuntimeError(output.read())
            yield ping, perf_counter() - started
        finally:
            if process.poll() is None:
                process.terminate()
                process.wait(timeout=10)


def post(text, creator):
    data = {"creator_id": creator}
    if text is not None:
        data["text"] = text
    started = perf_counter()
    response = requests.post(f"{URL}/submit", json=data, timeout=30)
    return response, (perf_counter() - started) * 1000


def profile():
    sys.path.insert(0, str(ROOT))
    import app
    import audit
    import config

    stage_times = {}

    def timed(function, name):
        def wrapped(*args, **kwargs):
            started = perf_counter()
            try:
                return function(*args, **kwargs)
            finally:
                stage_times[name] = (perf_counter() - started) * 1000
        return wrapped

    with tempfile.TemporaryDirectory() as scratch:
        log = Path(scratch) / "audit.jsonl"
        with patch.object(config, "AUDIT_LOG", log):
            app.detector.model_signal(TEXT)
            with (
                patch.object(app.detector, "model_signal", timed(app.detector.model_signal, "detector")),
                patch.object(audit, "log_decision", timed(audit.log_decision, "decision_log")),
                patch.object(audit, "log_request", timed(audit.log_request, "request_log")),
            ):
                started = perf_counter()
                response = app.app.test_client().post("/submit", json={"creator_id": "profile", "text": TEXT})
                elapsed = (perf_counter() - started) * 1000
                assert response.status_code == 200
    print(json.dumps({"http_status": response.status_code, "total_ms": elapsed,
                      "stages_ms": stage_times, "other_ms": elapsed - sum(stage_times.values())}))


def load():
    with running_server():
        for rate in (1, 10):
            started = perf_counter()
            for index in range(10):
                sleep(max(0, started + index / rate - perf_counter()))
                offset = perf_counter() - started
                response, duration = post(TEXT, f"stretch-load-{rate}")
                print(json.dumps({"target_rps": rate, "send_offset_s": offset,
                                  "http_status": response.status_code, "duration_ms": duration}))


def trial():
    log = ROOT / "logs" / "requests.jsonl"
    with running_server() as (ping, readiness):
        counts = [len(log.read_text().splitlines())]
        good, first_ms = post(TEXT, "stretch-second-trial")
        counts.append(len(log.read_text().splitlines()))
        bad, _ = post(None, "stretch-second-trial")
        lines = log.read_text().splitlines()
        counts.append(len(lines))
        print(json.dumps({"readiness_s": readiness, "first_submission_ms": first_ms,
                          "ping_status": ping.status_code, "ping_body": ping.json(),
                          "valid_status": good.status_code, "valid_body": good.json(),
                          "rejected_status": bad.status_code, "rejected_body": bad.json(),
                          "log_counts": counts, "records": [json.loads(line) for line in lines[-2:]]}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=("profile", "load", "trial"))
    args = parser.parse_args()
    {"profile": profile, "load": load, "trial": trial}[args.experiment]()
