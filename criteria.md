# Acceptance Criteria — Provenance Guard

These five criteria define my targets before implementation and detection experiments. Each criterion must pass in all three Unit 8 trials. I will preserve these original targets even if the service misses them.

## 1. Limit wrong accusations against human writers

Prepare a fixed set of 10 passages I wrote myself, including at least three examples of plain or formal writing. Submit all 10 passages through `POST /submit` in each trial.

**Target:** At most 1 of the 10 passages receives the high-confidence AI label in each trial.

**Why this target:** A wrong accusation can damage a writer's trust in the platform. I prioritize avoiding these accusations, while recognizing that this small sample cannot establish the service's overall accuracy.

## 2. Separate human and AI sample scores

Before testing, save five human-written passages and five unedited AI-generated passages. Match each human passage with an AI passage on the same topic and within 20% of its word count. Record the source of each passage.

Submit the same 10 passages in each trial and calculate the mean combined score for each group. Higher scores must indicate stronger AI-like characteristics.

**Target:** The AI group's mean combined score is at least 0.15 higher than the human group's mean in each trial.

**Why this target:** On a score scale from 0 to 1, a gap of 0.15 demands observable separation. Matching topic and approximate length reduces two possible explanations for the difference. This test checks these samples rather than proving reliable authorship detection.

## 3. Make every label reachable and cover the full score range

Test `scoring.py::score_to_label` directly with scores from 0.00 to 1.00 in increments of 0.01. Also test each configured label boundary and values 0.000001 above and below it, where those values remain within 0 to 1.

**Target:** Every tested score maps to exactly one of the three documented labels. All three labels appear at least once, and every returned label matches the exact wording and score ranges in the README.

**Why this target:** The label mapping must represent uncertainty and handle boundary values consistently. A missing or unreachable label would make the service's disclosure misleading even if both signals run correctly.

## 4. Record appeals and change submission status

Create five valid submissions through `POST /submit`. For each returned `content_id`, send one appeal containing a non-empty explanation through `POST /appeal`. Inspect the appeal responses and audit log.

**Target:** All five appeals return HTTP 200 and status `under_review`. Each appeal creates a new audit entry containing the correct `content_id`, the submitted reasoning, and the new status. The original decision remains available in the log.

**Why this target:** Writers need a dependable way to challenge a decision. Recording both the original decision and the appeal makes the sequence reviewable and prevents an appeal from silently erasing earlier evidence.

## 5. Reject invalid submissions clearly

Send six separate requests to `POST /submit`:

1. A request with `text` missing.
2. A request with `text` set to an empty string.
3. A request with `text` containing only spaces.
4. A request with `text` set to a number.
5. A request with valid text but no `creator_id`.
6. A request with valid text but an empty `creator_id`.

**Target:** All six requests return HTTP 400 with a JSON error explaining the invalid field. None returns a successful classification or creates a successful scored-submission entry. Afterward, a valid `POST /ping` request still returns HTTP 200.

**Why this target:** Invalid requests should receive useful feedback instead of fabricated scores or server crashes. Checking `/ping` afterward confirms that rejecting bad input leaves the service responsive.

---

## Unit 9 Capstone Acceptance Criteria

Provenance Guard · Shape A (Deploy and Instrument) · Path B (Local with Logs)

These are AI-assisted proposals for review. CodePath asks you to author the final targets and reasons before collecting results. Record three trials for each criterion before the improvement and three afterward.

### 1. Clean-checkout startup

Have a peer follow `RUNNING.md` from a fresh clone. Ask them to show how they can tell the service is ready. Capture the start command and the readiness response.

**Target:** Following the setup steps and single launch command in `RUNNING.md` from a fresh clone, a valid `POST /ping` returns HTTP 200 in each trial. The tester uses the prerequisites documented in `RUNNING.md` without additional setup instructions.

**Why this target:** HTTP 200 confirms the local service can receive and answer a request. Requiring the documented steps alone makes the setup reproducible for a classmate.

### 2. One structured record per request

Use one valid `POST /submit` request and one with `text` missing. Before sending them, have the viewer predict how many new records should appear. Match the requests individually to the new structured records. Use the log position immediately after the readiness check as the starting point for the count.

**Target:** The two sequential `POST /submit` requests produce exactly two new records in the structured request log, one after each request. Check the log count after readiness, after the valid submission, and after the rejected submission. Each submission must increase the count by exactly one.

**Why this target:** A missing record hides a request, and a duplicate inflates request and error counts. Checking after each submission catches both.

### 3. Response outcome matches its log record

Show the successful client response and its corresponding structured record side by side. Ask the viewer to find the same outcome field in both. Use one field consistently across trials.

**Target:** For the successful `POST /submit`, the HTTP status recorded in the matching structured request log entry equals the status shown by the client in every trial.

**Why this target:** A matching status lets someone reading the log verify what the client received after the terminal output is gone.

### 4. Elapsed time is usable

Show the elapsed-time field and its unit for the two submissions. Ask the viewer to identify which took longer. Compare the recorded values using the same unit.

**Target:** Both submission records contain a finite, nonnegative numeric duration in milliseconds in every trial.

**Why this target:** A common unit makes successful and rejected requests easy to compare. This target checks whether the timing can be used to investigate delays without assuming a speed limit for the local model.

### 5. Failure reason is visible in the log

Show the rejected request’s log entry first. Ask the viewer to identify why it was rejected. Then reveal the request with the missing `text` field and its client response. Save the actual rejection record as evidence.

**Target:** The rejected submission’s structured request record identifies that the required `text` field was missing in every trial. A generic rejection status alone does not meet this target.

**Why this target:** The rejection reason lets a reader diagnose the request from the log without needing the original submission or a copy of the client response.

### Demo order

Start from the documentation → predict the log count → send the two submissions → match each request to its record → compare the successful outcome and elapsed times → explain the rejection from its log before revealing its input.

Use the same setup, inputs, and scoring rules for comparable trials. Save actual responses and log lines as text.
