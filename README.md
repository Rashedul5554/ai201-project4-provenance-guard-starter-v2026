# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is a local backend service for estimating AI-like writing
patterns and allowing writers to challenge a decision. It cannot prove authorship.

1. `POST /submit` receives JSON containing `text` and `creator_id`.
2. It validates the input, returning HTTP 400 for missing, non-string, or
   whitespace-only fields. Text too short for the model also returns HTTP 400.
3. `detector.model_signal` measures predictability using local GPT-2 perplexity.
4. `stylometry.style_signal` measures sentence variation, vocabulary variety,
   and punctuation density.
5. `scoring.py::combine_signals` combines model, style, and optional draft-revision
   scores with weights 0.40, 0.40, and 0.20; `score_to_label` maps
   that result to a human, unsure, or AI label.
6. The route assigns a unique `content_id`, appends the decision to
   `logs/audit.jsonl`, and returns both signals, combined score, confidence,
   full label, guess, provenance score, any valid creator credential, and status `decided`.
7. `POST /appeal` accepts that ID and a writer's reasoning. It verifies a
   completed decision exists and appends an appeal with status `under_review`.
   The latest entry represents the current status; the original stays intact.

The appeal path acknowledges a request for review, not a completed human review.
Invalid appeal fields return HTTP 400; an unknown completed submission returns
HTTP 404. The code does not authenticate the claimed creator identity.

The starter environment check passed all nine checks on my Mac with Python 3.13.
The service runs locally; rate limiting remains disabled for Unit 7.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** GPT-2 perplexity: how predictable the text is to the local model. `detector.model_signal` maps it to 0–1, with higher scores indicating more AI-like predictability.

**Why that might differ between human and AI writing:** Generated text can favor predictable wording. This is a hypothesis behind the signal, not a reliable authorship test.

**What it can't see:** Authorship, the writing process, or the writer's intent. Plain human writing can be predictable; unusual AI wording can be unpredictable. It only examines up to the configured 400 model tokens.

### Signal two — the style signal

**What it measures:** Three text-shape features in `stylometry.py`:

- Sentence-length spread: population standard deviation of sentence word counts
  divided by their mean. Its AI-like component is `1 - min(spread, 1)`.
- Vocabulary variety: unique lowercase tokens divided by total tokens. Its
  AI-like component is `1 - type_token_ratio`.
- Punctuation density: Unicode punctuation characters divided by non-whitespace
  characters. Its AI-like component is `1 - min(density / 0.10, 1)`.

The style score weights these components 0.50, 0.30, and 0.20 respectively.
Fewer than 20 tokens or fewer than two usable sentences returns a neutral 0.5.
These constants are starting assumptions, not learned or validated parameters.

**Why that might differ between human and AI writing:** The initial heuristic assumes uniform sentence lengths, repeated vocabulary, and sparse punctuation can indicate AI-like style. Those patterns also occur in human writing and need evaluation.

**What it can't see:** Meaning or authorship. Typos, quotations, and editing can move the score. Vocabulary variety depends on passage length, punctuation depends on genre, and the starter word tokenizer poorly represents many non-English languages. A neutral short-text score is a fallback, not evidence of human or AI origin.

### Signal three — draft revision activity (bonus)

**What it measures:** `provenance.py::draft_signal` examines optional
`draft_history` metadata rather than the final text's predictability or style.
The list contains 1–10 non-empty draft strings, each at most 20,000 characters;
the last must exactly equal the submitted text.

For each adjacent pair, Python `SequenceMatcher` computes similarity with
`autojunk=False`. A meaningful revision has similarity between 0.50 and 0.98
inclusive AND a length change of at least 10 characters. Two or more meaningful
revisions yield score 0.20. Otherwise, including missing history, score is 0.50.
Malformed supplied history returns HTTP 400. No missing-history penalty implies
AI authorship; 0.50 represents no directional evidence.

**Why it might differ:** A recorded series of substantive revisions can support
a drafting process, while a pasted final answer may have no such history.
This is a deliberately weak process heuristic, not a learned detector.

**What it cannot see:** Whether the drafts were written by a person, generated
by AI, fabricated after the fact, or ordered truthfully. Genuine writers can
write in one pass and AI can generate convincing draft histories. It records
no trusted timestamps or editor events. It is independent in measured property,
not guaranteed statistically independent of the other signals.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** A weighted average of three different properties: model predictability (0.40), text style (0.40), and supplied draft-revision activity (0.20). The revision metadata has less weight because it can be fabricated. Strong disagreement can move the average toward uncertainty; no weighting proves authorship.

**The numbers:** `combined_score = 0.4 * model_score + 0.4 * style_score + 0.2 * provenance_score`.
The three weights live in `config.py`. Missing draft history receives a neutral
provenance score of 0.5, so an ordinary request uses
`0.4 * model_score + 0.4 * style_score + 0.1`.
Inputs must be finite and between 0 and 1; weights must be finite, nonnegative,
and sum to 1. The result is rounded to four decimal places. It is not a
calibrated probability of authorship.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**Historical two-signal comparison, before the bonus change:**

The original personal passage produced model score `0.8402` and style score
`0.3995`. The equal average was `0.6199`, so the final mapping returned
`unsure`. The actual response and matching log are pasted below.

**Confidence:** `max(combined_score, 1 - combined_score)`, rounded to four
decimal places. It measures heuristic directional strength from 0.5 to 1, not
the probability that the named label is correct. For an unsure result it still
reports the stronger direction; it is not confidence in an accusation.

**Historical calibration observations (old 0.50/0.50 rule):**

- Original AI time-management passage: model `0.4266`, style `0.6583`,
  combined `0.5424`; this lies in the unsure band.
- Original personal passage: model `0.8402`, style `0.3995`,
  combined `0.6199`; unsure.
- Original formal human passage: model `0.7728`, style `0.6124`,
  combined `0.6926`. The earlier route still returned a placeholder guess,
  but this score maps to AI under the final thresholds: a false positive.
- Human-edited AI passage: model `0.5197`, style `0.5390`,
  combined `0.5293`; this lies in the unsure band.

The edited AI passage was based on the AI-assisted biographical draft, not the
time-management passage, so these are not a controlled before/after pair.
The personal and formal text files were subsequently changed; their later scores
are for different inputs, not repeated measurements of the original passages.
The original personal request remains preserved in `results/milestone5_sample_run.json`.

**Historical submissions demonstrating reachable labels (old 0.50/0.50 rule):**

- Revised personal sample: `human`, combined `0.2465`.
- Revised formal sample: `unsure`, combined `0.3737`.
- AI-generated unusual-prose diagnostic: `human`, combined `0.1711`.
  This is a missed AI detection, not a genuinely human sample.
- AI-generated repetitive diagnostic: model `0.9943`, style `0.9255`,
  combined `0.9599`; `ai`.

These results demonstrate label reachability, not reliable accuracy. The
thresholds and weights were not changed to force those outcomes.
The diagnostics were deliberately selected to explore score ranges.
The saved response files and audit log provide the evidence; the Unit 8
three-trial evaluation has not been performed.

---

## Label Variants

Configured in `config.py` and implemented in `scoring.py::score_to_label`:

- **High-confidence human** (`guess: human`): `0 <= score <= 0.35`.
  Exact text: "This writing shows strong human-like patterns. This estimate does not verify who wrote it."
- **Unsure** (`guess: unsure`): `0.35 < score < 0.65`.
  Exact text: "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review."
- **High-confidence AI** (`guess: ai`): `0.65 <= score <= 1`.
  Exact text: "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review."

Every finite score from 0 to 1 maps to exactly one label. Scores outside that
range are rejected by the mapping. Boundary checks at 0, 0.35, 0.3501,
0.6499, 0.65, and 1 returned the expected categories.

**Why I worded the unsure label this way:** It directly admits uncertainty,
states that no wrongdoing has been established, and provides a review path.
The AI label also describes patterns rather than claiming proof of AI use.
The current 0.35/0.65 thresholds leave a middle band, but the observed formal
human false positive shows that this band does not eliminate wrong accusations.

---

## Sample Run

<!-- BONUS_SAMPLE_START -->
Actual three-signal submission and appeal, followed by content lookup. The credential token is omitted from published evidence. Requests were sent by `capture_bonus_evidence.py` using Python requests.

**POST /submit — HTTP 200**

```json
{
  "method": "POST",
  "path": "/submit",
  "request": {
    "text": "I checked the school laptop and recorded the fault. The wireless adapter was disabled after an update. I enabled the adapter and tested the connection again.",
    "creator_id": "rashedul",
    "draft_history": [
      "I checked the school laptop and recorded the fault.",
      "I checked the school laptop and recorded the fault. The wireless adapter was disabled after an update.",
      "I checked the school laptop and recorded the fault. The wireless adapter was disabled after an update. I enabled the adapter and tested the connection again."
    ],
    "verification_token": "<private creator-bound token supplied locally>"
  },
  "http_status": 200,
  "response": {
    "combined_score": 0.4342,
    "confidence": 0.5658,
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "guess": "unsure",
    "human_credential": {
      "badge": "Verified human — local reviewer check",
      "creator_id": "rashedul",
      "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
      "issued_at": 1793235908.41208,
      "reviewer": "MD ISLAM",
      "scope": "Creator completed an observed task; authorship of later items is not verified."
    },
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "model_score": 0.2773,
    "provenance_score": 0.2,
    "status": "decided",
    "style_score": 0.7081
  }
}
```
**GET /content/f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d — HTTP 200**

```json
{
  "method": "GET",
  "path": "/content/f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
  "request": null,
  "http_status": 200,
  "response": {
    "combined_score": 0.4342,
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "creator_id": "rashedul",
    "guess": "unsure",
    "human_credential": {
      "badge": "Verified human — local reviewer check",
      "creator_id": "rashedul",
      "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
      "issued_at": 1793235908.41208,
      "reviewer": "MD ISLAM",
      "scope": "Creator completed an observed task; authorship of later items is not verified."
    },
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "last_updated": "2026-10-29T01:05:20+00:00",
    "model_score": 0.2773,
    "provenance_score": 0.2,
    "status": "decided",
    "style_score": 0.7081,
    "timestamp": "2026-10-29T01:05:20+00:00"
  }
}
```
**POST /appeal — HTTP 200**

```json
{
  "method": "POST",
  "path": "/appeal",
  "request": {
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "reasoning": "Please review this diagnostic submission. The example draft text was supplied by AI; the creator credential is not proof of this item's authorship."
  },
  "http_status": 200,
  "response": {
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "message": "Your appeal has been recorded for review.",
    "status": "under_review"
  }
}
```
**GET /content/f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d — HTTP 200**

```json
{
  "method": "GET",
  "path": "/content/f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
  "request": null,
  "http_status": 200,
  "response": {
    "combined_score": 0.4342,
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "creator_id": "rashedul",
    "guess": "unsure",
    "human_credential": {
      "badge": "Verified human — local reviewer check",
      "creator_id": "rashedul",
      "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
      "issued_at": 1793235908.41208,
      "reviewer": "MD ISLAM",
      "scope": "Creator completed an observed task; authorship of later items is not verified."
    },
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "last_updated": "2026-10-29T01:05:20+00:00",
    "model_score": 0.2773,
    "provenance_score": 0.2,
    "status": "under_review",
    "style_score": 0.7081,
    "timestamp": "2026-10-29T01:05:20+00:00"
  }
}
```
**Matching audit entries (original decision and appeal)**

```json
[
  {
    "combined_score": 0.4342,
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "creator_id": "rashedul",
    "guess": "unsure",
    "human_credential": {
      "badge": "Verified human — local reviewer check",
      "creator_id": "rashedul",
      "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
      "issued_at": 1793235908.41208,
      "reviewer": "MD ISLAM",
      "scope": "Creator completed an observed task; authorship of later items is not verified."
    },
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "model_score": 0.2773,
    "provenance_score": 0.2,
    "status": "decided",
    "style_score": 0.7081,
    "timestamp": "2026-10-29T01:05:20+00:00"
  },
  {
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "creator_id": "rashedul",
    "event": "appeal",
    "reasoning": "Please review this diagnostic submission. The example draft text was supplied by AI; the creator credential is not proof of this item's authorship.",
    "status": "under_review",
    "timestamp": "2026-10-29T01:05:20+00:00"
  }
]
```

<!-- BONUS_SAMPLE_END -->

---

## How I Used AI

**Moment 1 — Planning and acceptance criteria**

- *What I asked for:* Help understanding the assignment, a draft of
  `planning.md`, and an updated `criteria.md`.
- *What came back:* AI drafted the submission flow, endpoint contracts, and
  all five proposed criteria with targets and reasons.
- *What I changed:* I added the supplied drafts to my repository and committed
  them before the implementation experiments. I have not documented independent
  changes to those criteria; I do not claim I authored the targets without AI.

**Moment 2 — Building and checking the service**

- *What I asked for:* Updated Python files, help interpreting terminal output,
  and help completing the Unit 7 implementation.
- *What came back:* AI supplied route code, the style heuristic, the combining
  rule, labels, appeal code, test commands, and README drafting assistance.
- *What I changed:* I applied the updates in stages, ran them locally, and
  returned the actual outputs for review. I asked to preserve Unit 8 code and
  limit today's work to Unit 7. The route progressed from a fixed response to
  model-only scoring, then two signals, and finally labels and logged appeals.

AI also supplied diagnostic passages and a biographical draft. The latter was
used as the basis for the edited-AI sample. I supplied the personal and formal
samples and subsequently revised their files. Generated or AI-assisted passages
are identified as such rather than counted as independently human-written.

The assignment asks students to author their own acceptance criteria. The AI
drafting above is disclosed because it does not meet that authorship instruction
as written; it should not be hidden or described as unaided work.


## Unit 7 Bonus Declaration — Before Implementation

I plan to add all three stretch features:
1. A third signal based on submitted draft revisions, weighted 0.20 alongside
   model predictability (0.40) and style (0.40). Draft history can be fabricated;
   this signal is evidence of revision activity, not proof of human authorship.
2. `GET /content/<id>` returning a decision and its latest status, including
   `under_review` after an appeal.
3. A verified-human path: a reviewer observes a live writing challenge and issues
   a creator-bound credential through a local reviewer command. The credential
   appears on later submissions when the writer supplies its secret token.
   This is a local demonstration, not production identity verification.

After implementation I will record real requests, responses, before/after appeal
status, and a credential-bearing item. I will distinguish demonstrations from
actual reviewer verification and keep all Unit 8 code unchanged.


## Unit 7 Bonus Implementation

The declaration above is preserved. Commit the declaration-only README before
copying these implementation files into the repository. Do not backdate commits.

### Content status lookup (+1 requested)

`GET /content/<id>` returns the original decision, public human credential if
present, latest status, and `last_updated`. After an appeal it shows
`under_review` while preserving the original scores and label. Unknown IDs return
HTTP 404. It does not expose the writer's appeal reasoning or credential token.

### Verified-human path (+1 requested)

1. The writer runs `python verification.py request --creator rashedul`.
2. A reviewer observes that writer read the random challenge phrase and compose
   a short original paragraph live, in person or on a live call, within 30 minutes.
3. Only after observing the task, the reviewer runs
   `python verification.py approve --reviewer "Actual reviewer name"`, then
   explicitly types `OBSERVED`. The one-use request is marked approved.
4. The local command creates a creator-bound random credential token, saving
   it in `.private/writer_credential.json`. Server state stores only its hash.
5. The writer supplies `verification_token` on a later `/submit` request with
   the same `creator_id`. A matching credential appears in the response, audit
   entry, and `/content/<id>` as `human_credential`, including badge text and ID.
   An invalid or mismatched token returns HTTP 403. Without a token, the field
   is null; a creator name alone cannot claim the credential.

Badge: **Verified human — local reviewer check**. The credential confirms an
observed task, not authorship of every later item. It never overrides scoring,
so a credential-bearing human can still receive an AI-like estimate and appeal.
There is no hosted identity service. Reviewer approval is protected by local
filesystem access, not a production administrator login. The credential does
not expire and there is no revocation UI yet. Keep `.private/` out of Git.
Do not describe an unobserved/self-approved demonstration as independent human
verification. The capture command requires a credential from the extra step.

### What changed

Two-signal scoring became 0.40 model + 0.40 style + 0.20 draft activity. The
model and style implementations, label thresholds, existing criteria, and Unit 8
rate limiting are unchanged. The lookup route reuses the append-only audit log.
Verification state is separate private local data. No third-party messages or
accounts are involved.

### Actual bonus evidence

<!-- BONUS_EVIDENCE_START -->
Actual local results are saved in `results/bonus_evidence.json`.

Labels observed under the new weights: ai, human, unsure.

The sample above shows a provenance score of 0.20, a creator credential on an item, and lookup moving from decided to under_review. Missing-history input returned 0.50. Unknown content returned 404; a token used with another creator returned 403.

Diagnostic texts were supplied by AI and were not the reviewer's live writing task. The badge does not attest to their authorship.

```json
{
  "creator_credential": {
    "badge": "Verified human — local reviewer check",
    "creator_id": "rashedul",
    "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
    "issued_at": 1793235908.41208,
    "reviewer": "MD ISLAM",
    "scope": "Creator completed an observed task; authorship of later items is not verified."
  },
  "lookup_before_appeal": {
    "combined_score": 0.4342,
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "creator_id": "rashedul",
    "guess": "unsure",
    "human_credential": {
      "badge": "Verified human — local reviewer check",
      "creator_id": "rashedul",
      "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
      "issued_at": 1793235908.41208,
      "reviewer": "MD ISLAM",
      "scope": "Creator completed an observed task; authorship of later items is not verified."
    },
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "last_updated": "2026-10-29T01:05:20+00:00",
    "model_score": 0.2773,
    "provenance_score": 0.2,
    "status": "decided",
    "style_score": 0.7081,
    "timestamp": "2026-10-29T01:05:20+00:00"
  },
  "lookup_after_appeal": {
    "combined_score": 0.4342,
    "content_id": "f55d53b4-dd7d-47aa-beb9-e8b04b8abe1d",
    "creator_id": "rashedul",
    "guess": "unsure",
    "human_credential": {
      "badge": "Verified human — local reviewer check",
      "creator_id": "rashedul",
      "credential_id": "de0430ce-ebfa-43a9-9aa7-a4d8682dcfe4",
      "issued_at": 1793235908.41208,
      "reviewer": "MD ISLAM",
      "scope": "Creator completed an observed task; authorship of later items is not verified."
    },
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "last_updated": "2026-10-29T01:05:20+00:00",
    "model_score": 0.2773,
    "provenance_score": 0.2,
    "status": "under_review",
    "style_score": 0.7081,
    "timestamp": "2026-10-29T01:05:20+00:00"
  },
  "diagnostic_requests_and_responses": [
    {
      "method": "GET",
      "path": "/content/no-such-id",
      "request": null,
      "http_status": 404,
      "response": {
        "error": "not_found",
        "message": "Content not found."
      }
    },
    {
      "method": "POST",
      "path": "/submit",
      "request": {
        "text": "I checked the school laptop and recorded the fault. The wireless adapter was disabled after an update. I enabled the adapter and tested the connection again.",
        "creator_id": "rashedul-other",
        "verification_token": "<private creator-bound token supplied locally>"
      },
      "http_status": 403,
      "response": {
        "error": "invalid_credential",
        "message": "Credential token is invalid for this creator."
      }
    },
    {
      "method": "POST",
      "path": "/submit",
      "request": {
        "text": "I checked the school laptop and recorded the fault. The wireless adapter was disabled after an update. I enabled the adapter and tested the connection again.",
        "creator_id": "bonus-no-draft"
      },
      "http_status": 200,
      "response": {
        "combined_score": 0.4942,
        "confidence": 0.5058,
        "content_id": "78ff9b9c-0bf9-496f-82dd-fe8ae9eb0a41",
        "guess": "unsure",
        "human_credential": null,
        "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
        "model_score": 0.2773,
        "provenance_score": 0.5,
        "status": "decided",
        "style_score": 0.7081
      }
    },
    {
      "method": "POST",
      "path": "/submit",
      "request": {
        "text": "Rain stopped. Beneath the viaduct, a watchmaker in saffron boots wrestled a buckled accordion case past the fishmonger's shutter, scattering receipts, brass washers, and a single bruised persimmon across the cobbles while a tram screeched somewhere uphill. Nobody claimed the fruit.",
        "creator_id": "ai-unusual-diagnostic"
      },
      "http_status": 200,
      "response": {
        "combined_score": 0.2369,
        "confidence": 0.7631,
        "content_id": "0605959b-3fb8-434c-9842-b09fb7cd7604",
        "guess": "human",
        "human_credential": null,
        "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
        "model_score": 0.1644,
        "provenance_score": 0.5,
        "status": "decided",
        "style_score": 0.1778
      }
    },
    {
      "method": "POST",
      "path": "/submit",
      "request": {
        "text": "The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results. The system is designed to provide clear and consistent results.",
        "creator_id": "ai-repetitive-diagnostic"
      },
      "http_status": 200,
      "response": {
        "combined_score": 0.8679,
        "confidence": 0.8679,
        "content_id": "b1bf1c99-f513-4d33-96fd-28117503bae9",
        "guess": "ai",
        "human_credential": null,
        "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
        "model_score": 0.9943,
        "provenance_score": 0.5,
        "status": "decided",
        "style_score": 0.9255
      }
    },
    {
      "method": "POST",
      "path": "/submit",
      "request": {
        "text": "Here,I write about myself in 5 bullet points:\n    1. I am a CSIS(Computer Science and Information Security) student at The City University of New York at John Jay college of Criminal Justice\n    2. I have been actively engaged with Undergraduate Research where my research background is Biophysics, Biochemistry and Cellular and Molecular biology since my major is Computere Science and informaiton security. \n    3. I have related Tech Job and internship expetiencs which is i used to work as a college assistant in Strategic Initivative Advancement (The College Website) Department where i worked as a Fontend developer build multiple From, process and wirte script usidg the software \"ProcessMaker\" and using the language HTML, CSS, and Javascript. \n    4. One of my Tech Related internship is  i am Departmen of Education (DOE) IT and Tech support intern where i manage and handel more then thousands device update the operatin system, manage and distridute schools devies and remotely manage and maintaince device by cloude system using Microsoft Intune Managmente systemr where i can actavite/deactivate, remiage, update, wipe and resate, deploy application to the device. \n    5. I love to do volunteering work specially social work. My current volunteer role is Victim Service Advocate at New York City Public Hospital where i help people who face domistic violence and sexual assulat i love to teach people about how to do their own advocacy and raise voice againest every crime. ",
        "creator_id": "human_personal.txt"
      },
      "http_status": 200,
      "response": {
        "combined_score": 0.2972,
        "confidence": 0.7028,
        "content_id": "13b4ef58-2749-4d25-b344-61792f7af28e",
        "guess": "human",
        "human_credential": null,
        "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
        "model_score": 0.2033,
        "provenance_score": 0.5,
        "status": "decided",
        "style_score": 0.2898
      }
    },
    {
      "method": "POST",
      "path": "/submit",
      "request": {
        "text": "I am a Computer Science and Inoformation Security major student at John jay college of Crimimal justice and my minor is Chemisriy. I actively engaged with undergraduare research, my research backgournd is biochemisry and Cellular and moluecular biology where i am focusing immunocell theraphy in therapetuic cancer treatemnt. Beside that, i am also doing a technical internship which is DOE IT and Tech Surreprt Internship where i provide technical  and informational related tasks.   ",
        "creator_id": "human_formal.txt"
      },
      "http_status": 200,
      "response": {
        "combined_score": 0.399,
        "confidence": 0.601,
        "content_id": "28f18643-b3bc-4c4f-a331-36778f85769c",
        "guess": "unsure",
        "human_credential": null,
        "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
        "model_score": 0.0287,
        "provenance_score": 0.5,
        "status": "decided",
        "style_score": 0.7187
      }
    }
  ]
}
```

<!-- BONUS_EVIDENCE_END -->

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

