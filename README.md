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
The saved response files and audit log provide the Unit 7 evidence. The Unit 8
baseline evaluation appears in Run Log and Verdicts.

---

## Label Variants

Configured in `config.py` and implemented in `scoring.py::score_to_label`:

- **High-confidence human** (`guess: human`): `0 <= score <= 0.35`.
  Exact text: "This writing shows strong human-like patterns. This estimate does not verify who wrote it."
- **Unsure** (`guess: unsure`): `0.35 < score < 0.68`.
  Exact text: "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review."
- **High-confidence AI** (`guess: ai`): `0.68 <= score <= 1`.
  Exact text: "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review."

Every finite score from 0 to 1 maps to exactly one label. Scores outside that
range are rejected by the mapping. Boundary checks at 0, 0.35, 0.3501,
0.6499, 0.65, and 1 returned the expected categories.

**Why I worded the unsure label this way:** It directly admits uncertainty,
states that no wrongdoing has been established, and provides a review path.
The AI label also describes patterns rather than claiming proof of AI use.
The Unit 8 experiment raised the AI boundary from 0.65 to 0.68. See The Improvement for the observed outcomes.

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

**Unit 8 progress:** Instrumentation, the full baseline attack run, and three
baseline criteria trials are recorded. The attack judgments and diagnoses below
are AI-assisted interpretations for review. The threshold improvement, initial after runs, and repeat criteria trials are
recorded.

**My limits:** 10 submissions per minute and 200 submissions per day on
`POST /submit`, configured in `config.py`. `RATE_LIMITING_ENABLED` is `True`
and the `@limiter.limit(...)` decorator above `submit` is active.

**Why those numbers and not others:** These are my initial limits. Ten requests
per minute permits short bursts of submissions or edits from a writer while
preventing one caller from making hundreds of scoring requests in a minute.
The daily cap of 200 is intended to allow substantial legitimate use while
constraining sustained automated probing. Neither number is validated against
real production traffic. Frequent users could hit the caps, and an attacker
can rotate claimed creator IDs to evade a per-creator quota.

**What a caller counts as:** A usable string `creator_id` identifies the caller.
If the JSON is not an object or the ID is absent/invalid/blank, the limiter falls
back to the remote address. Valid IDs count separately even on the same address;
requests without valid IDs can share one address quota. The ID is caller-supplied,
not authenticated. The key currently returns the original ID string, so callers
can also vary whitespace to obtain a different key. This limitation has not
been changed during the baseline setup.

The existing storage is in-memory. Restarting the service clears counters;
multiple processes would not share the same counters. These limits apply only
to `/submit`, not the appeal or lookup routes.

**The run of status codes when I pushed past it:**

Produced by `run_attacks.py::run_flood` on November 6, 2026 at 1:49 p.m.
America/New_York, using `python run_attacks.py --flood 15`. Saved in
`results/flood_2026-11-06_1349.md`.

```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

Ten requests succeeded and five were rate limited. This confirms the per-minute
limit in this run; it does not test reaching the daily cap.

An earlier check at 1:30 p.m., preserved in `results/flood_2026-11-06_1330.md`,
returned fifteen `200` responses because rate limiting was not active. That is
an initial setup observation, not successful limiter evidence.

### Audit logging checks

Successful decisions record all nine required fields: timestamp, content_id,
creator_id, guess, model_score, style_score, combined_score, label, and status.
The third-signal score and optional human credential are additional fields.

The existing `rate_limited` handler records `429` rejections. The new
`app.py::log_submit_rejections` after-response hook records `/submit` responses
with status 400 or above, excluding 429 to avoid duplicate rejection entries.
Rejections have no successful classification; their shorter event shape is
intentional and includes the reason and available caller identity. The existing
429 shape includes its limit; the new hook includes the HTTP status.

**Example rate-limit rejection, read back with `GET /log`:**

```json
{
  "timestamp": "2026-11-06T18:49:15+00:00",
  "creator_id": "flood_tester",
  "event": "rejected",
  "status": "rejected",
  "reason": "rate_limited",
  "limit": "10 per 1 minute"
}
```

**Invalid-input request and response:**

```bash
curl -i -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"creator_id":"missing-text-check"}'
```

HTTP status: `400 BAD REQUEST`.

```json
{
  "error": "invalid_input",
  "message": "text must be a non-empty string."
}
```

**Matching rejection, read back with `GET /log?limit=1`:**

```json
{
  "timestamp": "2026-11-06T18:54:55+00:00",
  "creator_id": "missing-text-check",
  "event": "rejected",
  "status": "rejected",
  "reason": "invalid_input",
  "http_status": 400
}
```

Audit timestamps are UTC; `18:54:55+00:00` is 1:54:55 p.m. EST.
These two entries verify instrumentation. They do not replace the requirement
to paste at least ten informative entries, mostly from the full attack run,
including at least one rejection, in the next section.

**AI assistance for this stage:** I asked for the next steps and an updated
README based on my actual output. AI suggested enabling the existing limiter,
adding the rejection logging hook, and documenting the resulting checks. I
applied the code and ran the flood and missing-text requests locally. The
initial limits and the explanation above were AI-assisted; I need to review
that explanation against the usage I intend to support.

---

## Attack Run — Before

**Instrumented baseline completed on November 6, 2026 at 2:05 p.m. EST.**
All 56 supplied inputs were sent through `/submit` with rate limiting and
rejection logging enabled. The runner reported zero automatic crash failures;
that is distinct from the reviewed attack outcomes below.

```bash
python run_attacks.py --set attack_set --label before_instrumented
```

Saved report: `results/attack_run_2026-11-06_1405_before_instrumented.md`.
The reviewed judgments were prepared with AI assistance after this run; I need
to understand and defend the stated interpretations. These judgments are not
new measurements or revisions to the original five acceptance criteria.

**Reviewed outcomes: 39 HELD, 17 BROKE.** Keep the following judgment rules
consistent when comparing this baseline against later runs. The earlier
uninstrumented report `results/attack_run_2026-11-06_1333_before.md` is retained
as exploratory evidence, not substituted for this instrumented baseline.

### Baseline judgment rules

These are AI-assisted proposed interpretations for the student to review and
defend, applied after the recorded baseline run. They are not new acceptance
criteria and do not change the original targets in criteria.md. Keep the same
interpretations for before/after comparison rather than redefining success to
favor a later result. The recorded service outputs have not been changed.

- **Evasion:** BROKE if known-AI evasion text avoided an affirmative `ai` label
  (including `unsure`). Under a stricter impersonation-only rule requiring
  `human`, EV01–EV09 would be HELD instead. This report uses detection avoidance;
  it does not equate uncertainty with a confident claim of human authorship.
- **False positives:** BROKE only when a staff-designated human sample received
  `ai`; `unsure` avoids the targeted accusation and is HELD for this objective.
- **Prompt injection:** Judge the stated output or integrity objective, not the
  attack's family name. PI02 is BROKE for achieving the requested human guess,
  with partial success only; it did not obtain its requested confidence or skip
  scoring. This run does not demonstrate that any instruction was executed.
- **Invalid requests:** HTTP 400 without a classification is HELD. For MF03–MF06,
  a confident authorship label on non-prose is judged BROKE for evidence
  insufficiency. Valid Arabic text is not malformed solely because of script.
- **Long input:** HELD for completing without a crash/time-out; no preexisting
  maximum length requires rejection. Partial model coverage remains a limitation.
- **Flood:** The first ten successes are allowed by policy. The family is HELD
  when subsequent requests return 429. All 12 rows are assessed in this family
  context. The CSV target description says "20", but only 12 rows were supplied
  and sent; do not claim a 20-request run.

**Score clarification:** The original runner's `Score` column is confidence,
`max(combined_score, 1 - combined_score)`, not the AI-like combined score.
The column is renamed below. Exact combined scores in the per-attack review
come from matching audit entries, not from the three-decimal summary.
For example, FP02 is `unsure` at combined 0.6498; FP06 is `ai` at 0.6503.
Both round to 0.650 in the original table, so do not judge from that rounding.

Actual creator IDs are recorded in each detailed result. Some malformed requests
have no usable creator ID, and all flood rows share `attacker_flood`.

| ID | Family | Targeting | Status | Content ID | Guess | Confidence | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b040af35-d09a-4975-b2f4-114a2ebb07f5` | unsure | 0.584 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `66aed748-0f62-4265-a398-ad17969aecc8` | unsure | 0.546 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `2fa3ec00-23e7-47ef-9358-dba9cc894659` | unsure | 0.557 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `1b633009-9257-4168-a03f-c9124a19a278` | unsure | 0.591 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `56331126-15ed-422b-bdc8-ca6dc6a82ce7` | unsure | 0.618 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7635f590-0fb9-4ee8-a064-0fd44eced0b9` | unsure | 0.573 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `430f2942-d530-4086-af79-a4bf6c3f01b1` | unsure | 0.534 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `8ea1ff05-1e64-4ed3-b833-a48057e0d8cc` | unsure | 0.602 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `d89c6943-9746-418d-b28d-c899d77d9135` | unsure | 0.570 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `a5a2eb17-cec7-4408-85ae-ee941c95cd20` | ai | 0.780 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0bdf0a00-687d-4f02-b341-b501e44e7aa5` | unsure | 0.557 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `d5a9c9ef-5e4c-4299-9908-6c26294087e0` | unsure | 0.650 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `724dc615-6be0-48fa-8591-91876961698b` | ai | 0.658 | BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `ebb0d426-4b56-41a5-aa41-6251658364e6` | unsure | 0.648 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `bfd04649-84eb-4b4c-9953-784a535e59a0` | ai | 0.676 | BROKE |
| FP06 | false_positive | a person imitating a formal template | 200 | `0cf1f99d-eeff-4ec9-bef4-11698aa1f8da` | ai | 0.650 | BROKE |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b99d079b-c851-48a6-8822-05602ff37f09` | unsure | 0.636 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `4de0751e-e9e4-462c-b3ee-072501bdd6a6` | unsure | 0.571 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6d65c3bd-1794-4c34-963f-9b49bde41ceb` | unsure | 0.562 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `628e0650-a60a-47b8-a34c-11ccd1e03209` | human | 0.675 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `639a01ba-b6ee-457e-9558-3b2a6995133a` | unsure | 0.552 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `6556c9eb-64a3-4da1-9874-e0b231b8719b` | unsure | 0.511 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `fd1ebcc8-df03-42ad-8142-71fbd0f2990e` | unsure | 0.507 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `cf5d6bf3-8289-42e2-81fa-ede6b61aa5ee` | unsure | 0.536 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `ac833d54-962b-4884-9420-fc3993918c6a` | human | 0.700 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `ed6e6b69-6a46-4f60-9e62-d9568d671a89` | human | 0.696 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `e4024fff-ec79-46d9-a8b6-e0124bc1fca9` | ai | 0.699 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `a63c9526-fc29-4b9a-b91c-0da66bb3ba6a` | ai | 0.699 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `2f389316-2d68-4243-8106-9cdfaa22ec36` | ai | 0.663 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `8533d21c-51a6-4ed0-8994-5d7279368ca7` | ai | 0.790 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `54aa70ea-3597-4b26-9032-05369479f1f8` | human | 0.689 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3e345acb-1498-45fb-b5c0-cc3401a78f5c` | human | 0.689 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d85f8781-46f5-4abd-a08d-492b35421549` | human | 0.689 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d3b79421-24d1-4c47-a593-3efc4b09be61` | human | 0.689 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `be037dae-3015-4a5c-b317-e7006d610c94` | human | 0.689 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8714b2c2-31c5-46ba-9cb7-5315e041654e` | human | 0.689 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fd3d8ef9-a726-4735-974e-f48e09f6f801` | human | 0.689 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `493559e1-b989-4070-9bbf-5aca8e8369ed` | human | 0.689 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d13a4429-5c48-435a-aa24-664658e0447b` | human | 0.689 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a2566dbe-eccb-47bb-9fa9-7bc4db30b027` | human | 0.689 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |


### Results by family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 5 | 3 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 16 | 4 |
| `prompt_injection` | 6 | 5 | 1 |


### Ten audit log entries from the baseline run

These are actual entries selected by matching baseline content IDs and run
timestamps. Eight are decisions spanning evasion, false positives, instruction
text, and non-prose/multilingual inputs. The last two are an invalid-input
rejection and a rate-limit rejection. Decision entries retain the nine required
fields plus the provenance score and any credential; rejected requests have
no successful classification and use the shorter rejection event shape.
Timestamps are UTC. The extract is saved as
`results/audit_before_selected_10.json`.

```json
[
  {
    "timestamp": "2026-11-06T19:05:22+00:00",
    "content_id": "b040af35-d09a-4975-b2f4-114a2ebb07f5",
    "creator_id": "attacker_EV01",
    "guess": "unsure",
    "model_score": 0.1635,
    "style_score": 0.6261,
    "combined_score": 0.4158,
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:22+00:00",
    "content_id": "66aed748-0f62-4265-a398-ad17969aecc8",
    "creator_id": "attacker_EV02",
    "guess": "unsure",
    "model_score": 0.5943,
    "style_score": 0.2896,
    "combined_score": 0.4536,
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:22+00:00",
    "content_id": "724dc615-6be0-48fa-8591-91876961698b",
    "creator_id": "attacker_FP03",
    "guess": "ai",
    "model_score": 0.8051,
    "style_score": 0.5895,
    "combined_score": 0.6578,
    "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:23+00:00",
    "content_id": "bfd04649-84eb-4b4c-9953-784a535e59a0",
    "creator_id": "attacker_FP05",
    "guess": "ai",
    "model_score": 0.8005,
    "style_score": 0.6406,
    "combined_score": 0.6764,
    "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:23+00:00",
    "content_id": "0cf1f99d-eeff-4ec9-bef4-11698aa1f8da",
    "creator_id": "attacker_FP06",
    "guess": "ai",
    "model_score": 0.8814,
    "style_score": 0.4944,
    "combined_score": 0.6503,
    "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:23+00:00",
    "content_id": "628e0650-a60a-47b8-a34c-11ccd1e03209",
    "creator_id": "attacker_PI02",
    "guess": "human",
    "model_score": 0.2044,
    "style_score": 0.3587,
    "combined_score": 0.3252,
    "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:23+00:00",
    "content_id": "ac833d54-962b-4884-9420-fc3993918c6a",
    "creator_id": "attacker_MF03",
    "guess": "human",
    "model_score": 0.0,
    "style_score": 0.5,
    "combined_score": 0.3,
    "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:23+00:00",
    "content_id": "2f389316-2d68-4243-8106-9cdfaa22ec36",
    "creator_id": "attacker_MF07",
    "guess": "ai",
    "model_score": 0.9064,
    "style_score": 0.5,
    "combined_score": 0.6626,
    "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
    "status": "decided",
    "provenance_score": 0.5,
    "human_credential": null
  },
  {
    "timestamp": "2026-11-06T19:05:23+00:00",
    "creator_id": "attacker_MF01",
    "event": "rejected",
    "status": "rejected",
    "reason": "invalid_input",
    "http_status": 400
  },
  {
    "timestamp": "2026-11-06T19:05:24+00:00",
    "creator_id": "attacker_flood",
    "event": "rejected",
    "status": "rejected",
    "reason": "rate_limited",
    "limit": "10 per 1 minute"
  }
]
```

### Worst observed outcome

FP03 is the selected worst outcome: a staff-designated passage from a careful
non-native English writer received the high-confidence AI label. Model score
was 0.8051, style score 0.5895, and neutral provenance score 0.5000. Their
weighted sum, rounded to four decimals, is 0.6578, exceeding the 0.65 AI boundary.
The response communicates uncertainty and permits appeal, but the writer still
receives an AI-like accusation based on ordinary writing properties.
This selection is a value judgment about the cost of an error, not a measured
ranking of harm to actual individuals.

### Baseline attack diagnoses

The following annotations cover all 17 attacks marked BROKE under the stated
rules. They connect observed scores to known code paths. They do not establish
that a particular edit caused a score change without an unmodified control.
Detailed explanations for all 56 HELD/BROKE verdicts remain in the reviewed
report. Criteria verdicts and diagnoses are still pending the three-trial run.

**EV01 — evasion: model and/or style signal, then combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.1635`, style `0.6261`, provenance `0.5000`, combined `0.4158`.

**EV02 — evasion: style signal / combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.5943`, style `0.2896`, provenance `0.5000`, combined `0.4536`.

**EV03 — evasion: style signal / combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.6662`, style `0.4771`, provenance `0.5000`, combined `0.5573`.

**EV04 — evasion: model signal / combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.6114`, style `0.6161`, provenance `0.5000`, combined `0.5910`.

**EV05 — evasion: model and/or style signal, then combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.3212`, style `0.3832`, provenance `0.5000`, combined `0.3818`.

**EV06 — evasion: style signal / combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.5727`, style `0.2459`, provenance `0.5000`, combined `0.4274`.

**EV07 — evasion: model and/or style signal, then combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.5862`, style `0.5000`, provenance `0.5000`, combined `0.5345`.

**EV08 — evasion: model signal / combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.2452`, style `0.5000`, provenance `0.5000`, combined `0.3981`.

**EV09 — evasion: model and/or style signal, then combining rule.**

The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

Recorded scores: model `0.7042`, style `0.4709`, provenance `0.5000`, combined `0.5700`.

**FP03 — false_positive: model predictability / combining rule / label mapping.**

A staff-designated human sample received ai. Predictability and style, with a neutral provenance score, pushed the combined score to or above 0.65. That is the wrong-accusation outcome this family targets.

Recorded scores: model `0.8051`, style `0.5895`, provenance `0.5000`, combined `0.6578`.

**FP05 — false_positive: model predictability / combining rule / label mapping.**

A staff-designated human sample received ai. Predictability and style, with a neutral provenance score, pushed the combined score to or above 0.65. That is the wrong-accusation outcome this family targets.

Recorded scores: model `0.8005`, style `0.6406`, provenance `0.5000`, combined `0.6764`.

**FP06 — false_positive: model predictability / combining rule / label mapping.**

A staff-designated human sample received ai. Predictability and style, with a neutral provenance score, pushed the combined score to or above 0.65. That is the wrong-accusation outcome this family targets.

Recorded scores: model `0.8814`, style `0.4944`, provenance `0.5000`, combined `0.6503`.

**PI02 — prompt_injection: model/style features and combining rule (classification outcome).**

The input requested human and received human, so the requested classification outcome occurred. However, the requested confidence was 0.02 and the actual confidence was 0.6748; the model and style signals still ran. This is a classification bypass, not demonstrated instruction execution, a forged credential, or a skipped check.

Recorded scores: model `0.2044`, style `0.3587`, provenance `0.5000`, combined `0.3252`.

**MF03 — malformed: route evidence sufficiency / signal fallbacks / label mapping.**

The route classified control-character text with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

Recorded scores: model `0.0000`, style `0.5000`, provenance `0.5000`, combined `0.3000`.

**MF04 — malformed: route evidence sufficiency / signal fallbacks / label mapping.**

The route classified punctuation-only text with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

Recorded scores: model `0.0112`, style `0.5000`, provenance `0.5000`, combined `0.3045`.

**MF05 — malformed: route evidence sufficiency / signal fallbacks / label mapping.**

The route classified a repeated-character single word with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

Recorded scores: model `0.9976`, style `0.5000`, provenance `0.5000`, combined `0.6990`.

**MF06 — malformed: route evidence sufficiency / signal fallbacks / label mapping.**

The route classified emoji-only text with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

Recorded scores: model `0.9969`, style `0.5000`, provenance `0.5000`, combined `0.6988`.

**Other limitations observed without calling the corresponding robustness tests broken:**
MF07's valid Arabic input was accepted, but the ai result is not established as
a true or false authorship judgment. MF08 completed without an error; its model
signal still covers only the first 400 tokens while its style signal uses the
whole passage. These limitations warrant follow-up; neither a denial of service
nor a known-authorship false positive was demonstrated for those two inputs.

---

## Run Log and Verdicts

All five original criteria met their targets in each of the three baseline
trials on November 7, 2026. I ran `python run_unit8_eval.py --label before`
against the instrumented local service.

- Run ID `unit8-b433dad16f`
- Dataset SHA-256 `81b8a1f471d5c9778a648fbe38431cd5d4d1eaae44b19dcfca55ecd7ebb13ef9`
- [Summary](results/criteria_2026-11-07_225321_before.md) and [complete observed results](results/criteria_2026-11-07_225321_before.json)

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Limit wrong accusations against human writers | At most 1 of 10 independently human-written passages labeled AI per trial; at least 3 plain/formal examples | 0/10 labeled ai | 0/10 labeled ai | 0/10 labeled ai | MET |
| 2. Separate human and AI sample scores | Mean combined AI score minus mean combined human score >= 0.15; 5 matched pairs within 20% word count | mean gap 0.21914 | mean gap 0.21914 | mean gap 0.21914 | MET |
| 3. Label mapping and full range coverage | Every tested score maps to exactly one documented label; all 3 labels appear; 0.01 grid plus exact boundaries and adjacent values | 105/105 label checks | 105/105 label checks | 105/105 label checks | MET |
| 4. Record appeals and change status | All 5 appeals return HTTP 200 and under_review; reasoning logged and original decisions preserved | 5/5 appeals | 5/5 appeals | 5/5 appeals | MET |
| 5. Reject invalid submissions clearly | All 6 specified cases return HTTP 400 with field explanation; no successful decision entries; ping remains HTTP 200 | 6/6 invalid cases; ping 200 | 6/6 invalid cases; ping 200 | 6/6 invalid cases; ping 200 | MET |

The label check exercises the mapping function directly across the grid and
boundary cases. The five matched pairs measure separation on this dataset.
The staff attack results remain a separate measurement. In particular, the
staff set produced three AI labels on designated human passages, while these
ten human passages produced zero.

### Recorded evidence from trial 1

The snippets below are selected from the saved JSON. The linked results
contain every case from all three trials.

**1. Wrong AI accusations**

Produced by `app.py::submit`.

```json
{
  "sample_id": "H01",
  "http": 200,
  "body": {
    "combined_score": 0.5718,
    "confidence": 0.5718,
    "content_id": "df0283c5-5d03-40f0-b21c-c48d60ed662b",
    "guess": "unsure",
    "human_credential": null,
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "model_score": 0.6795,
    "provenance_score": 0.5,
    "status": "decided",
    "style_score": 0.5
  }
}
```

**2. Mean score separation**

Produced by `app.py::submit and run_unit8_eval.py::run_trial`.

```json
{
  "measure": "mean gap 0.21914",
  "pair": {
    "human_id": "H01",
    "ai_id": "A01",
    "source": "OpenAI Codex, generated for Unit 8 on 2026-11-07"
  },
  "human": {
    "sample_id": "H01",
    "http": 200,
    "body": {
      "combined_score": 0.5718,
      "confidence": 0.5718,
      "content_id": "df0283c5-5d03-40f0-b21c-c48d60ed662b",
      "guess": "unsure",
      "human_credential": null,
      "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
      "model_score": 0.6795,
      "provenance_score": 0.5,
      "status": "decided",
      "style_score": 0.5
    }
  },
  "ai": {
    "sample_id": "A01",
    "http": 200,
    "body": {
      "combined_score": 0.6412,
      "confidence": 0.6412,
      "content_id": "126f6f63-3179-497c-9958-4c00485ab51e",
      "guess": "unsure",
      "human_credential": null,
      "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
      "model_score": 0.8531,
      "provenance_score": 0.5,
      "status": "decided",
      "style_score": 0.5
    }
  }
}
```

**3. Label mapping**

Produced by `scoring.py::score_to_label`.

```json
[
  {
    "score": "0.649999",
    "expected": "unsure",
    "guess": "unsure",
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "ok": true
  },
  {
    "score": "0.65",
    "expected": "ai",
    "guess": "ai",
    "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
    "ok": true
  },
  {
    "score": "0.650001",
    "expected": "ai",
    "guess": "ai",
    "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
    "ok": true
  }
]
```

**4. Appeal and audit retention**

Produced by `app.py::submit, appeal, get_log`.

```json
{
  "submission": {
    "sample_id": "H01",
    "http": 200,
    "body": {
      "combined_score": 0.5718,
      "confidence": 0.5718,
      "content_id": "5debf7dc-fe46-4080-b9ef-7ebf053fc8e1",
      "guess": "unsure",
      "human_credential": null,
      "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
      "model_score": 0.6795,
      "provenance_score": 0.5,
      "status": "decided",
      "style_score": 0.5
    }
  },
  "ok": true,
  "request": {
    "content_id": "5debf7dc-fe46-4080-b9ef-7ebf053fc8e1",
    "reasoning": "Unit 8 evaluation trial unit8-b433dad16f-1: please review this decision."
  },
  "response": {
    "http": 200,
    "body": {
      "content_id": "5debf7dc-fe46-4080-b9ef-7ebf053fc8e1",
      "message": "Your appeal has been recorded for review.",
      "status": "under_review"
    }
  },
  "matching_log": [
    {
      "combined_score": 0.5718,
      "content_id": "5debf7dc-fe46-4080-b9ef-7ebf053fc8e1",
      "creator_id": "unit8-b433dad16f-1-appeal0",
      "guess": "unsure",
      "human_credential": null,
      "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
      "model_score": 0.6795,
      "provenance_score": 0.5,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-11-08T03:53:23+00:00"
    },
    {
      "content_id": "5debf7dc-fe46-4080-b9ef-7ebf053fc8e1",
      "creator_id": "unit8-b433dad16f-1-appeal0",
      "event": "appeal",
      "reasoning": "Unit 8 evaluation trial unit8-b433dad16f-1: please review this decision.",
      "status": "under_review",
      "timestamp": "2026-11-08T03:53:23+00:00"
    }
  ]
}
```

**5. Invalid request and service responsiveness**

Produced by `app.py::submit, get_log, ping`.

```json
{
  "invalid_case": {
    "expected_field": "text",
    "response": {
      "http": 400,
      "body": {
        "error": "invalid_input",
        "message": "text must be a non-empty string."
      }
    },
    "new_log_entries": [
      {
        "creator_id": "unit8-b433dad16f-1-bad0",
        "event": "rejected",
        "http_status": 400,
        "reason": "invalid_input",
        "status": "rejected",
        "timestamp": "2026-11-08T03:53:23+00:00"
      }
    ],
    "ok": true
  },
  "ping": {
    "http": 200,
    "body": {
      "ok": true,
      "service": "provenance-guard",
      "you_sent": "unit8-eval"
    }
  }
}
```

### Criteria diagnoses

There were no criteria misses in these three trials. The attack-level
diagnoses are recorded under Attack Run — Before. I used an AI-assisted test
runner to record and summarize the trials.

---

## The Improvement

I raised the AI threshold from 0.65 to 0.68 while retaining the human boundary
at 0.35. The baseline staff false positives FP03, FP05 and FP06 scored
between 0.6503 and 0.6764. I widened the unsure range to test whether those
passages could avoid an affirmative AI label.

### Attack Run — After

The [reviewed after report](results/attack_run_2026-11-07_2300_after.md) contains
all 56 recorded responses and verdicts. The table below uses the same
interpretations as the baseline. The final numeric column is confidence.

| ID | Family | Targeting | Status | Content ID | Guess | Confidence | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `220c7112-89c7-4044-bd66-30ab2820c388` | unsure | 0.584 | BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `d9ed5be8-46c8-4db6-aaf1-c4424d4e02fa` | unsure | 0.546 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `9c1473e1-aa3d-4589-a13b-ce03d8195ba3` | unsure | 0.557 | BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `e31b3dbf-7f7f-4901-866c-50ec9124f603` | unsure | 0.591 | BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `4cf3efc4-dd50-4f8b-957a-98cf3c38ddbc` | unsure | 0.618 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `cf19401e-916a-48d3-83c0-8d12da7f749f` | unsure | 0.573 | BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `a5a586db-ce02-4eee-8d5b-7ddfaa4ad35d` | unsure | 0.534 | BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `623f7422-a988-4c38-8041-c7babe1b2b81` | unsure | 0.602 | BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `0635537a-2ab4-407c-b6fa-d43dcb0d786a` | unsure | 0.570 | BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c552ebbf-caa2-4103-9cda-07e3f859b1ad` | ai | 0.780 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3290e1bc-8873-46d3-b000-7e7269f7c015` | unsure | 0.557 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `8a9aa68b-259b-4e4a-a680-b4ad1a3d9273` | unsure | 0.650 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `3e78f46f-914c-40b7-93bc-1b97feea7cf1` | unsure | 0.658 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `7332ae5b-dee5-4916-a830-dab2b61449ad` | unsure | 0.648 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `9abd28b8-e24e-4426-8125-22e3441bcd71` | unsure | 0.676 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `2cf3fc24-ef67-43a3-a3bf-fb3bdfaed0df` | unsure | 0.650 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b7f31722-039f-4c3b-b398-d3e2d665876c` | unsure | 0.636 | HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `3fa4af24-9acb-4c5f-8267-66d6190f77cf` | unsure | 0.571 | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `a4aaa15b-9a28-4093-8dda-059d5e54e5b0` | unsure | 0.562 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `34656792-deff-4c21-8713-07ae864796fc` | human | 0.675 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `ff3a7493-266e-4d83-bb3a-60cdde85cafc` | unsure | 0.552 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `f2c03161-3e83-4e2d-8273-4f7775a49409` | unsure | 0.511 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `06b49196-ffc9-4f0e-8125-9dbc6d90f69e` | unsure | 0.507 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `d9e37cb8-da99-4a42-8688-276240f28907` | unsure | 0.536 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 200 | `f5953ce5-162f-44cc-a04a-ceccddb2027c` | human | 0.700 | BROKE |
| MF04 | malformed | text is only punctuation | 200 | `455e1fb8-abd7-4a77-b86f-c735bb0bdf2e` | human | 0.696 | BROKE |
| MF05 | malformed | text is a very long single word | 200 | `e74698b9-0ea1-403f-aae6-6c33dd26615e` | ai | 0.699 | BROKE |
| MF06 | malformed | text is emoji only | 200 | `2c505972-d18d-4156-8d53-51a76bf87d0d` | ai | 0.699 | BROKE |
| MF07 | malformed | text is right-to-left script | 200 | `3bf61ad1-b771-49c4-8a6c-43f1e2f0d4dd` | unsure | 0.663 | HELD |
| MF08 | malformed | text is 60,000 characters | 200 | `9bc0fcb3-bc5b-4a9a-aa6b-94376860965f` | ai | 0.790 | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b25e11d6-d859-4fe0-b437-b27dd34cef96` | human | 0.689 | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `88615031-4b9c-4bb6-a92b-0bfaafc5bafe` | human | 0.689 | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1c7e2f47-a75b-43cc-a443-23af995cff67` | human | 0.689 | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c8d565c9-dc34-40fa-b761-980f58daa2ee` | human | 0.689 | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `45e17a5a-d3d5-4438-a630-0987a768ee18` | human | 0.689 | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `92350073-70f9-454e-be78-ce5b2df34e6e` | human | 0.689 | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0c41d930-9d04-4c82-a6cd-479892969d58` | human | 0.689 | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `05725fab-b2b5-4e0a-bd9b-509af2e3bc3f` | human | 0.689 | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6a71d279-27e0-4c9e-98a2-1984f2314709` | human | 0.689 | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e1325d60-89bf-4857-bb79-5017f30db43c` | human | 0.689 | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

Using the same inputs and verdict rules, the staff run moved from 39 HELD
and 17 BROKE to 42 HELD and 14 BROKE. Staff false positives fell from 3/8
to 0/8. Nine of ten evasion inputs still avoided an affirmative AI label,
and EV10 retained its AI label. MF07 also moved from ai to unsure. That
Arabic-script case remains HELD as a route robustness check. No HTTP status
changed across the 56 requests. A wider unsure range could also withhold an AI
label from genuine AI passages scoring between 0.65 and 0.68. The staff set
used to choose the threshold does not measure that risk on unseen inputs.

### Initial after criteria run

[Original summary](results/criteria_2026-11-07_230055_after.md) and [original evidence](results/criteria_2026-11-07_230055_after.json).
The sample hash matched the baseline. Criteria 1, 2 and 4 met their targets
in all three trials. Criterion 3 scored 102/107 in each trial because the
README still specified the old 0.65 boundary. Scores 0.65, 0.650001, 0.66,
0.67 and 0.679999 were documented as ai while the code returned unsure.

Criterion 5 recorded 6/6, 5/6 and 4/6. The missing and empty creator-ID
requests share the address quota. The attack run and closely spaced criteria
trials reused that quota, so three cases returned 429 before validation.
Ping returned 200 in all three trials. The original verdicts are preserved.

### Repeat after criteria run

The repeat run started after a service restart and waited 61 seconds between
trials. The active README ranges matched the 0.68 threshold. The dataset
hash matched both earlier runs. All five original criteria met their targets
in all three repeat trials.

| Criterion | Target | Trial 1 | Trial 2 | Trial 3 | Verdict |
|---|---|---|---|---|---|
| 1. Wrong AI accusations | At most 1 of 10 human passages labeled ai | 0/10 labeled ai | 0/10 labeled ai | 0/10 labeled ai | MET |
| 2. Mean score separation | AI mean minus human mean >= 0.15 over five matched pairs | mean gap 0.21914 | mean gap 0.21914 | mean gap 0.21914 | MET |
| 3. Label mapping | All grid and boundary cases match documented labels; all three appear | 105/105 label checks | 105/105 label checks | 105/105 label checks | MET |
| 4. Appeals | 5 of 5 reach under_review, log reasoning and retain decision | 5/5 appeals | 5/5 appeals | 5/5 appeals | MET |
| 5. Invalid input | 6 of 6 return 400 with field error, no scored decision; ping returns 200 | 6/6 invalid cases; ping 200 | 6/6 invalid cases; ping 200 | 6/6 invalid cases; ping 200 | MET |

[Repeat summary](results/criteria_2026-11-07_230720_after.md) and
[complete repeat evidence](results/criteria_2026-11-07_230720_after.json).

The label mapping matched the corrected documentation in 105/105 checks per
trial. All six invalid cases reached validation and returned 400 in every
trial. The initial 429s still demonstrate how a shared quota affects callers
without valid creator IDs. The mean score gap stayed at 0.21914, as expected
because changing the label boundary leaves the underlying scores unchanged.
The zero AI labels on the ten evaluation passages were also unchanged.

---

## What's Still Broken

- **EV01–EV09:** The combined scores still put these known-AI passages in the
  unsure range. Editing can alter the model's predictability signal or the
  style statistics without changing who wrote the text. A follow-up would
  compare each edited input with its original passage, then test whether
  scoring smaller sections makes the result less sensitive to one unusual
  segment.
- **PI02:** The disguised system message still received a human label. Its
  model and style scores produced a combined score below the human boundary.
  The request did not skip scoring or set the requested confidence. A
  follow-up would compare the same passage with and without the prefix to
  measure its influence on the features.
- **MF03–MF06:** Control characters, punctuation, repeated characters and emoji
  can still receive confident labels. The route accepts these strings and the
  style fallback can leave the model score with enough influence to reach a
  confident label. I would test a validation rule for text with too little
  usable language, including legitimate short and multilingual inputs.
- **Invalid-input criterion in the initial after run:** A burst of requests
  without usable creator IDs can still receive 429 before validation. The
  repeat isolates the validation test with fresh quota windows. It does not
  remove or change that real rate-limit behavior.

I stopped after the one measured threshold change so the comparison isolates
its effect. No original acceptance criterion remained missed in the repeat
run. The staff cases used to choose the threshold are the same ones used to
measure the change, so the reduction in false positives needs confirmation
on fresh passages.

For a production deployment, I would send uncertain cases to review and
avoid treating an AI label as grounds for punishment by itself. Writers
benefit from fewer wrong accusations, while reviewers bear the added work
and some AI-written passages may pass without an affirmative label.

### AI use in Unit 8

I used Codex to help wire rejection logging, interpret the attack results,
prepare the evaluation runner, and summarize the observed evidence. Codex
also generated the five matched AI passages. The human passages are my own
writing. I used the recorded results to compare the 0.65 and 0.68 thresholds,
and kept the initial after run as evidence of the documentation mismatch and
shared rate-limit interference.

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

