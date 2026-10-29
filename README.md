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
5. `scoring.py::combine_signals` averages both scores; `score_to_label` maps
   that result to a human, unsure, or AI label.
6. The route assigns a unique `content_id`, appends the decision to
   `logs/audit.jsonl`, and returns both signals, combined score, confidence,
   full label, guess, and status `decided`.
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

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** An equal weighted average. Neither signal has demonstrated greater reliability yet. Strong opposing scores move the average toward uncertainty; moderate disagreement can still yield a confident label.

**The numbers:** `combined_score = 0.5 * model_score + 0.5 * style_score`.
Keep `WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5` in `config.py`.
Inputs must be finite and between 0 and 1; weights must be finite, nonnegative,
and sum to 1. The result is rounded to four decimal places. It is not a
calibrated probability of authorship.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**

The original personal passage produced model score `0.8402` and style score
`0.3995`. The equal average was `0.6199`, so the final mapping returned
`unsure`. The actual response and matching log are pasted below.

**Confidence:** `max(combined_score, 1 - combined_score)`, rounded to four
decimal places. It measures heuristic directional strength from 0.5 to 1, not
the probability that the named label is correct. For an unsure result it still
reports the stronger direction; it is not confidence in an accusation.

**Calibration observations:**

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
The original personal request remains preserved in the Sample Run evidence.

**Actual submissions demonstrating reachable labels:**

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

Actual successful submission and appeal captured in
`results/milestone5_sample_run.json`. These requests were sent with Python
`requests`; the full JSON bodies and responses are pasted here as text.
Timestamps in the log are UTC.

**Submission request**

`POST http://127.0.0.1:5000/submit`, `Content-Type: application/json`

```json
{
  "text": "Here,I write about myself in 5 bullet points:\n    1. I am a Computer Science and Information Security (CSIS) student at John Jay College of Criminal Justice, The City University of New York (CUNY).\n    2. I have been actively involved in undergraduate research, with a background in biophysics, biochemistry, and cellular and molecular biology. My research experience has allowed me to explore scientific fields beyond my primary area of study.\n    3. I have hands-on experience in technology through my work as a College Assistant in the Strategic Initiative Advancement Department, where I contributed to the college website as a frontend developer. I built forms, developed workflows, and wrote scripts using ProcessMaker, HTML, CSS, and JavaScript.\n    4. I have also worked as an IT and Tech Support Intern with the New York City Department of Education (DOE). In this role, I helped manage thousands of devices, update operating systems, distribute and maintain school devices, and remotely manage devices through Microsoft Intune. My responsibilities included activating and deactivating devices, reimaging, updating, wiping, resetting, and deploying applications.\n    5. I am passionate about volunteering, especially in social services. I currently serve as a Victim Service Advocate at a New York City public hospital, where I support survivors of domestic violence and sexual assault. I also help people understand their rights, advocate for themselves, and find the confidence to speak up against violence and injustice.",
  "creator_id": "human-personal"
}
```

**Submission response — HTTP 200**

```json
{
  "combined_score": 0.6199,
  "confidence": 0.6199,
  "content_id": "a8fdf6b2-04ae-4259-9b06-97021faea227",
  "guess": "unsure",
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "model_score": 0.8402,
  "status": "decided",
  "style_score": 0.3995
}
```

**Appeal request**

`POST http://127.0.0.1:5000/appeal`, `Content-Type: application/json`

```json
{
  "content_id": "a8fdf6b2-04ae-4259-9b06-97021faea227",
  "reasoning": "I wrote this sample myself and request a review."
}
```

**Appeal response — HTTP 200**

```json
{
  "content_id": "a8fdf6b2-04ae-4259-9b06-97021faea227",
  "message": "Your appeal has been recorded for review.",
  "status": "under_review"
}
```

**Log request**

`GET http://127.0.0.1:5000/log` returned HTTP 200. The matching entries
for the submission ID are pasted below; other submissions were filtered out.

```json
[
  {
    "combined_score": 0.6199,
    "content_id": "a8fdf6b2-04ae-4259-9b06-97021faea227",
    "creator_id": "human-personal",
    "guess": "unsure",
    "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
    "model_score": 0.8402,
    "status": "decided",
    "style_score": 0.3995,
    "timestamp": "2026-10-29T00:04:17+00:00"
  },
  {
    "content_id": "a8fdf6b2-04ae-4259-9b06-97021faea227",
    "creator_id": "human-personal",
    "event": "appeal",
    "reasoning": "I wrote this sample myself and request a review.",
    "status": "under_review",
    "timestamp": "2026-10-29T00:04:17+00:00"
  }
]
```

The original entry remains `decided`; the later appeal records the item's
new status as `under_review`.

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

