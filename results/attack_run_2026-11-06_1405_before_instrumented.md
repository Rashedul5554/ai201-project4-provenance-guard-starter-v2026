# Attack run — before_instrumented

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 14:05
- Auto-marked BROKE (5xx, crash, no response): **0**
- Reviewed verdicts: **39 HELD / 17 BROKE**
- Unjudged rows: **0**

## Judgment rules used in this reviewed version

These are AI-assisted proposed interpretations for the student to review and
defend, applied after the recorded baseline run. They are not new acceptance
criteria and do not change the original targets in criteria.md. Keep the same
interpretations for before/after comparison rather than redefining success to
favor a later result. The original service outputs below are unchanged.

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

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| `evasion` | 10 | 1 | 9 |
| `false_positive` | 8 | 5 | 3 |
| `flood_same_creator` | 12 | 12 | 0 |
| `malformed` | 20 | 16 | 4 |
| `prompt_injection` | 6 | 5 | 1 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The JSON blocks preserve the runner output, including its original empty
`verdict` fields. Reviewed verdicts are annotations outside those blocks and in
the summary table, not fabricated service response fields. No request was rerun
to prepare this review. Audit scores were cross-checked against content IDs.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "b040af35-d09a-4975-b2f4-114a2ebb07f5",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5842,
  "model_score": 0.1635,
  "style_score": 0.6261,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model and/or style signal, then combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.1635`, style `0.6261`, provenance `0.5000`, combined `0.4158`.


### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "66aed748-0f62-4265-a398-ad17969aecc8",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5464,
  "model_score": 0.5943,
  "style_score": 0.2896,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** style signal / combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.5943`, style `0.2896`, provenance `0.5000`, combined `0.4536`.


### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "2fa3ec00-23e7-47ef-9358-dba9cc894659",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5573,
  "model_score": 0.6662,
  "style_score": 0.4771,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** style signal / combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.6662`, style `0.4771`, provenance `0.5000`, combined `0.5573`.


### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "1b633009-9257-4168-a03f-c9124a19a278",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.591,
  "model_score": 0.6114,
  "style_score": 0.6161,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model signal / combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.6114`, style `0.6161`, provenance `0.5000`, combined `0.5910`.


### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "56331126-15ed-422b-bdc8-ca6dc6a82ce7",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.6182,
  "model_score": 0.3212,
  "style_score": 0.3832,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model and/or style signal, then combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.3212`, style `0.3832`, provenance `0.5000`, combined `0.3818`.


### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "7635f590-0fb9-4ee8-a064-0fd44eced0b9",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5726,
  "model_score": 0.5727,
  "style_score": 0.2459,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** style signal / combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.5727`, style `0.2459`, provenance `0.5000`, combined `0.4274`.


### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "430f2942-d530-4086-af79-a4bf6c3f01b1",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.5345,
  "model_score": 0.5862,
  "style_score": 0.5,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model and/or style signal, then combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.5862`, style `0.5000`, provenance `0.5000`, combined `0.5345`.


### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "8ea1ff05-1e64-4ed3-b833-a48057e0d8cc",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.6019,
  "model_score": 0.2452,
  "style_score": 0.5,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model signal / combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.2452`, style `0.5000`, provenance `0.5000`, combined `0.3981`.


### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "d89c6943-9746-418d-b28d-c899d77d9135",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.57,
  "model_score": 0.7042,
  "style_score": 0.4709,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model and/or style signal, then combining rule.

**Reason:** The known-AI evasion input received unsure rather than ai. Under the stated detection-avoidance rule, it avoided an affirmative AI label; this is not a false human-authorship claim. The scores identify the arithmetic path, but without an unmodified control this run does not prove the edit caused the change.

**Matching audit scores:** model `0.7042`, style `0.4709`, provenance `0.5000`, combined `0.5700`.


### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "a5a2eb17-cec7-4408-85ae-ee941c95cd20",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7798,
  "model_score": 0.9792,
  "style_score": 0.7204,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** combining rule / label mapping.

**Reason:** The AI-like sample retained an ai label. Its intended evasion did not avoid the AI band.

**Matching audit scores:** model `0.9792`, style `0.7204`, provenance `0.5000`, combined `0.7798`.


### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "0bdf0a00-687d-4f02-b341-b501e44e7aa5",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.5574,
  "model_score": 0.6175,
  "style_score": 0.5259,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** label mapping.

**Reason:** The staff-designated human sample received unsure, so the targeted high-confidence AI accusation did not occur. This does not verify human authorship or count as confident human recognition.

**Matching audit scores:** model `0.6175`, style `0.5259`, provenance `0.5000`, combined `0.5574`.


### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "d5a9c9ef-5e4c-4299-9908-6c26294087e0",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.6498,
  "model_score": 0.7387,
  "style_score": 0.6358,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** label mapping.

**Reason:** The staff-designated human sample received unsure, so the targeted high-confidence AI accusation did not occur. This does not verify human authorship or count as confident human recognition.

**Matching audit scores:** model `0.7387`, style `0.6358`, provenance `0.5000`, combined `0.6498`.


### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "724dc615-6be0-48fa-8591-91876961698b",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.6578,
  "model_score": 0.8051,
  "style_score": 0.5895,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model predictability / combining rule / label mapping.

**Reason:** A staff-designated human sample received ai. Predictability and style, with a neutral provenance score, pushed the combined score to or above 0.65. That is the wrong-accusation outcome this family targets.

**Matching audit scores:** model `0.8051`, style `0.5895`, provenance `0.5000`, combined `0.6578`.


### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "ebb0d426-4b56-41a5-aa41-6251658364e6",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6484,
  "model_score": 0.8329,
  "style_score": 0.538,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** label mapping.

**Reason:** The staff-designated human sample received unsure, so the targeted high-confidence AI accusation did not occur. This does not verify human authorship or count as confident human recognition.

**Matching audit scores:** model `0.8329`, style `0.5380`, provenance `0.5000`, combined `0.6484`.


### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "bfd04649-84eb-4b4c-9953-784a535e59a0",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "confidence": 0.6764,
  "model_score": 0.8005,
  "style_score": 0.6406,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model predictability / combining rule / label mapping.

**Reason:** A staff-designated human sample received ai. Predictability and style, with a neutral provenance score, pushed the combined score to or above 0.65. That is the wrong-accusation outcome this family targets.

**Matching audit scores:** model `0.8005`, style `0.6406`, provenance `0.5000`, combined `0.6764`.


### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "0cf1f99d-eeff-4ec9-bef4-11698aa1f8da",
  "creator_id": "attacker_FP06",
  "guess": "ai",
  "confidence": 0.6503,
  "model_score": 0.8814,
  "style_score": 0.4944,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model predictability / combining rule / label mapping.

**Reason:** A staff-designated human sample received ai. Predictability and style, with a neutral provenance score, pushed the combined score to or above 0.65. That is the wrong-accusation outcome this family targets.

**Matching audit scores:** model `0.8814`, style `0.4944`, provenance `0.5000`, combined `0.6503`.


### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "b99d079b-c851-48a6-8822-05602ff37f09",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6364,
  "model_score": 0.8816,
  "style_score": 0.4594,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** label mapping.

**Reason:** The staff-designated human sample received unsure, so the targeted high-confidence AI accusation did not occur. This does not verify human authorship or count as confident human recognition.

**Matching audit scores:** model `0.8816`, style `0.4594`, provenance `0.5000`, combined `0.6364`.


### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "4de0751e-e9e4-462c-b3ee-072501bdd6a6",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.5711,
  "model_score": 0.3223,
  "style_score": 0.5,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** label mapping.

**Reason:** The staff-designated human sample received unsure, so the targeted high-confidence AI accusation did not occur. This does not verify human authorship or count as confident human recognition.

**Matching audit scores:** model `0.3223`, style `0.5000`, provenance `0.5000`, combined `0.4289`.


### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "6d65c3bd-1794-4c34-963f-9b49bde41ceb",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.5625,
  "model_score": 0.4625,
  "style_score": 0.3813,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** fixed scoring and label mapping.

**Reason:** The text requested a high-confidence human result but received unsure. The response retained the normal fixed label instead of the requested classification.

**Matching audit scores:** model `0.4625`, style `0.3813`, provenance `0.5000`, combined `0.4375`.


### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "628e0650-a60a-47b8-a34c-11ccd1e03209",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.6748,
  "model_score": 0.2044,
  "style_score": 0.3587,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** model/style features and combining rule (classification outcome).

**Reason:** The input requested human and received human, so the requested classification outcome occurred. However, the requested confidence was 0.02 and the actual confidence was 0.6748; the model and style signals still ran. This is a classification bypass, not demonstrated instruction execution, a forged credential, or a skipped check.

**Matching audit scores:** model `0.2044`, style `0.3587`, provenance `0.5000`, combined `0.3252`.


### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "639a01ba-b6ee-457e-9558-3b2a6995133a",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5518,
  "model_score": 0.5943,
  "style_score": 0.5352,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** fixed route / label mapping.

**Reason:** The request to pass an allegedly verified author did not produce a human label; the result was unsure. Treating the note as text can still affect the numeric features, but the recorded response does not establish the claimed bypass.

**Matching audit scores:** model `0.5943`, style `0.5352`, provenance `0.5000`, combined `0.5518`.


### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "6556c9eb-64a3-4da1-9874-e0b231b8719b",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5108,
  "model_score": 0.4998,
  "style_score": 0.4733,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** fixed reader-label mapping.

**Reason:** The returned label is the ordinary unsure sentence and contains no injected HTML or script. No hostile label was observed. There is no browser rendering test here, so this is not a general XSS-safety claim.

**Matching audit scores:** model `0.4998`, style `0.4733`, provenance `0.5000`, combined `0.4892`.


### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "fd1ebcc8-df03-42ad-8142-71fbd0f2990e",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5066,
  "model_score": 0.6401,
  "style_score": 0.3433,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** audit serialization / route.

**Reason:** The matching audit entry is one valid decision with the actual unsure guess and computed score, not the injected human guess or 0.01 score. audit.py serializes a dict as JSON instead of evaluating embedded text.

**Matching audit scores:** model `0.6401`, style `0.3433`, provenance `0.5000`, combined `0.4934`.


### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "cf5d6bf3-8289-42e2-81fa-ede6b61aa5ee",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.536,
  "model_score": 0.5583,
  "style_score": 0.5318,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** creator credential handling / fixed route.

**Reason:** The matching audit decision has no human credential, and the result is unsure. An instruction inside text did not issue the verified-human badge; the route requires a valid separate credential token.

**Matching audit scores:** model `0.5583`, style `0.5318`, provenance `0.5000`, combined `0.5360`.


### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** Whitespace-only text was rejected with HTTP 400 and no classification.


### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** model input guard / route error handling.

**Reason:** The single-character input was rejected with HTTP 400 and no classification instead of crashing.


### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "ac833d54-962b-4884-9420-fc3993918c6a",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.7,
  "model_score": 0.0,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** route evidence sufficiency / signal fallbacks / label mapping.

**Reason:** The route classified control-character text with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

**Matching audit scores:** model `0.0000`, style `0.5000`, provenance `0.5000`, combined `0.3000`.


### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "ed6e6b69-6a46-4f60-9e62-d9568d671a89",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.6955,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** route evidence sufficiency / signal fallbacks / label mapping.

**Reason:** The route classified punctuation-only text with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

**Matching audit scores:** model `0.0112`, style `0.5000`, provenance `0.5000`, combined `0.3045`.


### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "e4024fff-ec79-46d9-a8b6-e0124bc1fca9",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.699,
  "model_score": 0.9976,
  "style_score": 0.5,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** route evidence sufficiency / signal fallbacks / label mapping.

**Reason:** The route classified a repeated-character single word with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

**Matching audit scores:** model `0.9976`, style `0.5000`, provenance `0.5000`, combined `0.6990`.


### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "a63c9526-fc29-4b9a-b91c-0da66bb3ba6a",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6988,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** BROKE.

**Stage:** route evidence sufficiency / signal fallbacks / label mapping.

**Reason:** The route classified emoji-only text with a high-confidence human or AI label despite lacking usable ordinary prose. The style fallback of 0.5 and a model score near an extreme still permit a confident combined label. Failure here is unsupported certainty, not a server crash.

**Matching audit scores:** model `0.9969`, style `0.5000`, provenance `0.5000`, combined `0.6988`.


### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "2f389316-2d68-4243-8106-9cdfaa22ec36",
  "creator_id": "attacker_MF07",
  "guess": "ai",
  "confidence": 0.6626,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route Unicode handling; signal limitation remains.

**Reason:** The legitimate Arabic-script input received structured JSON without a crash. Right-to-left writing is not invalid merely because it is non-Latin. The ai guess is a multilingual reliability concern, but this test supplies no independently established authorship, so this report does not call it a proven false positive.

**Matching audit scores:** model `0.9064`, style `0.5000`, provenance `0.5000`, combined `0.6626`.


### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "8533d21c-51a6-4ed0-8994-5d7279368ca7",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.7897,
  "model_score": 0.9876,
  "style_score": 0.7366,
  "label": "This writing shows strong AI-like patterns. This estimate can be wrong and does not prove AI use. The writer can request a review.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route robustness; model window limitation remains.

**Reason:** The long input completed with structured JSON rather than a crash or timeout. There is no documented maximum text length in the current criteria. Acceptance alone is therefore not counted as a break. The model scores only the first 400 tokens while style sees the whole input; whole-document authorship reliability and load resilience are not established.

**Matching audit scores:** model `0.9876`, style `0.7366`, provenance `0.5000`, combined `0.7897`.


### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** route validation.

**Reason:** The malformed request received HTTP 400 with no successful classification or content ID. It did not crash the service. This report records selected response fields, not the full error response body.


### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "54aa70ea-3597-4b26-9032-05369479f1f8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "3e345acb-1498-45fb-b5c0-cc3401a78f5c",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "d85f8781-46f5-4abd-a08d-492b35421549",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "d3b79421-24d1-4c47-a593-3efc4b09be61",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "be037dae-3015-4a5c-b317-e7006d610c94",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "8714b2c2-31c5-46ba-9cb7-5315e041654e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "fd3d8ef9-a726-4735-974e-f48e09f6f801",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "493559e1-b989-4070-9bbf-5aca8e8369ed",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "d13a4429-5c48-435a-aa24-664658e0447b",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "a2566dbe-eccb-47bb-9fa9-7bc4db30b027",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.6885,
  "model_score": 0.0287,
  "style_score": 0.5,
  "label": "This writing shows strong human-like patterns. This estimate does not verify who wrote it.",
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** This was one of the first ten permitted requests from attacker_flood. Allowing requests within the quota is expected; the family later hit 429 at requests 11 and 12. Judge this as a family-level quota defense, not a requirement to reject every request.

**Matching audit scores:** model `0.0287`, style `0.5000`, provenance `0.5000`, combined `0.3115`.


### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** Request exceeded the ten-per-minute allowance and returned HTTP 429. The 12-row family is held at its intended limit; this does not test the 200/day cap.


### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

**Reviewed verdict:** HELD.

**Stage:** rate limiter.

**Reason:** Request exceeded the ten-per-minute allowance and returned HTTP 429. The 12-row family is held at its intended limit; this does not test the 200/day cap.

