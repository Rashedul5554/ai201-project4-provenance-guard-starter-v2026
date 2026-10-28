# Provenance Guard — Unit 7 Plan

## Purpose

Provenance Guard will accept a piece of writing and return an estimate of whether it appears human-written or AI-generated. It will communicate uncertainty and allow a writer to challenge a decision.

The signals cannot prove authorship. A wrong accusation can harm a real writer, so uncertain results should receive an "unsure" label.

This document describes the planned service. It does not report completed features or test results.

## 1. Submission Flow

1. Receive a JSON request at `POST /submit` containing `text` and `creator_id`.
2. Validate that both fields contain non-empty strings. Reject invalid input with a clear error.
3. Create a unique `content_id` for the submission.
4. Run the provided model signal in `detector.py`.
5. Run a separate style signal in `stylometry.py`.
6. Combine the two signal scores using `scoring.py::combine_signals`, then map the result to a label using `scoring.py::score_to_label`.
7. Save the decision through `audit.py` and return the submission ID, scores, guess, confidence, label, and status.

## 2. The Two Signals

### Signal One: Model Predictability

The provided local model measures how predictable the writing is. Predictable language may resemble model-generated writing.

Its limitation is that predictable language is also common in genuine human writing. Plain language, formal writing, and writing by someone using a second language could be incorrectly flagged. This signal cannot verify who wrote the text.

### Signal Two: Writing Style

I plan to measure sentence-length variation, the proportion of unique words, and punctuation density. I will combine these measurements into one style score.

These properties may differ between writing samples, but they are not proof of authorship. Short passages can produce unstable measurements. Typos, quotations, and editing can change the score without changing who wrote the text.

### Combining the Signals

Both scores will use the same direction: higher values indicate stronger AI-like characteristics.

I will document the combining rule, weights, and thresholds before implementing them. The settings will live in `config.py`.

The combined score will be an engineering estimate, not a verified probability of authorship. I will document how the response's confidence value relates to that score.

## 3. Handling a Wrong Accusation

A real writer could receive a high AI-like score because their writing is predictable and stylistically consistent.

The label should communicate an estimate without accusing the writer of cheating. The writer can appeal using the submission's `content_id` and an explanation.

An appeal will change the item's status to `under_review` and add an audit entry linked to the original decision. It will acknowledge the request without claiming that a human has already reviewed it or automatically changing the authorship estimate.

## 4. Planned Endpoint Contracts

### POST /submit

Required request fields:

- `text`: a non-empty string containing the writing.
- `creator_id`: a non-empty string identifying the submitting writer.

Successful response fields:

- `content_id`: unique submission identifier.
- `guess`: `human`, `unsure`, or `AI`.
- `confidence`: a number between 0 and 1, with its calculation documented.
- `label`: the full sentence shown to a reader.
- `model_score`: the normalized model signal score.
- `style_score`: the normalized style signal score.
- `combined_score`: the result of the combining rule.
- `status`: initially `scored`.

Invalid requests will return HTTP 400 with an explanatory error. A signal failure will return an error rather than a fabricated successful score.

### POST /appeal

Required request fields:

- `content_id`: an existing submission identifier.
- `reasoning`: a non-empty string explaining the appeal.

Successful response fields:

- `content_id`: the appealed submission identifier.
- `status`: `under_review`.
- `message`: confirmation that the appeal was recorded.

Missing or invalid fields will return HTTP 400. An unknown submission identifier will return HTTP 404.

## 5. Before Implementation

I will write five acceptance criteria in `criteria.md`, each with a measurable target and a reason. I will commit them before running detection experiments.

As I build, I will record actual requests, responses, and audit entries in the README. I will also document how I used AI and which suggestions I reviewed or changed.