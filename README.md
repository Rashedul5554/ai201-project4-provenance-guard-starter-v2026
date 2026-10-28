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

**Current progress: Milestone 4 implementation, awaiting an integrated run.**
Final labels, confidence, and appeals are not implemented yet. This is not a
completed Unit 7 submission.

1. `POST /submit` receives JSON with `text` and `creator_id`.
2. The route rejects missing, non-string, or whitespace-only fields with HTTP 400.
3. `detector.model_signal` measures predictability using local GPT-2 perplexity.
4. `stylometry.style_signal` measures sentence variation, vocabulary variety,
   and punctuation density.
5. `scoring.combine_signals` averages the two scores using configured weights.
6. The route assigns a unique ID and writes both scores and the combined score
   to `logs/audit.jsonl` through `audit.log_decision`.
7. It returns the ID and scores. For now, `guess` is `unsure`, `confidence` is
   `null`, and `status` is `partial_analysis`. These are development placeholders.

The planned final stage maps the combined score to one of three reader-facing
labels and supports a logged appeal that changes status to `under_review`.

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



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

**The rule:** An equal weighted average. Neither signal has demonstrated greater reliability yet. Strong opposing scores move the average toward uncertainty; moderate disagreement can still yield a confident label once mapping is connected.

**The numbers:** `combined_score = 0.5 * model_score + 0.5 * style_score`.
Keep `WEIGHT_MODEL_SIGNAL = 0.5` and `WEIGHT_STYLE_SIGNAL = 0.5` in `config.py`.
Inputs must be finite and between 0 and 1; weights must be finite, nonnegative,
and sum to 1. The result is rounded to four decimal places. It is not a
calibrated probability of authorship.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:**
The same grocery-store sample was tested separately: the model returned
`0.7483`; the style signal returned `0.5233`. They differ by `0.2250` in strength.
The equal average would be `0.6358`; this is calculated from those separate
runs, not yet captured from the integrated endpoint. With the current starter
thresholds (human at or below 0.35, AI at or above 0.65), this falls in the unsure
band once label mapping is connected.

The sample was supplied by AI during development. It is not evidence of
human authorship and must not be counted among passages I wrote myself.



---

## Label Variants

**Pending Milestone 5:** the code still contains placeholder labels. The table
below must be completed with the implemented text and exact boundary rules.

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

**Pending:** capture a real integrated submission, then a real appeal after
Milestone 5. Empty response blocks below are not test evidence.

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

AI assistance included setup troubleshooting, a planning draft, proposed
acceptance criteria, and Python implementation suggestions. The two moment
prompts below still need my own account of what I reviewed and changed. I must
not describe AI-generated criteria or sample passages as independently written.

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

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
