# Attack run — before_instrumented

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 14:05
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `b040af35-d09a-4975-b2f4-114a2ebb07f5` | unsure | 0.584 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `66aed748-0f62-4265-a398-ad17969aecc8` | unsure | 0.546 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `2fa3ec00-23e7-47ef-9358-dba9cc894659` | unsure | 0.557 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `1b633009-9257-4168-a03f-c9124a19a278` | unsure | 0.591 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `56331126-15ed-422b-bdc8-ca6dc6a82ce7` | unsure | 0.618 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `7635f590-0fb9-4ee8-a064-0fd44eced0b9` | unsure | 0.573 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `430f2942-d530-4086-af79-a4bf6c3f01b1` | unsure | 0.534 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `8ea1ff05-1e64-4ed3-b833-a48057e0d8cc` | unsure | 0.602 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `d89c6943-9746-418d-b28d-c899d77d9135` | unsure | 0.570 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `a5a2eb17-cec7-4408-85ae-ee941c95cd20` | ai | 0.780 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `0bdf0a00-687d-4f02-b341-b501e44e7aa5` | unsure | 0.557 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `d5a9c9ef-5e4c-4299-9908-6c26294087e0` | unsure | 0.650 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `724dc615-6be0-48fa-8591-91876961698b` | ai | 0.658 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `ebb0d426-4b56-41a5-aa41-6251658364e6` | unsure | 0.648 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `bfd04649-84eb-4b4c-9953-784a535e59a0` | ai | 0.676 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `0cf1f99d-eeff-4ec9-bef4-11698aa1f8da` | ai | 0.650 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `b99d079b-c851-48a6-8822-05602ff37f09` | unsure | 0.636 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `4de0751e-e9e4-462c-b3ee-072501bdd6a6` | unsure | 0.571 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `6d65c3bd-1794-4c34-963f-9b49bde41ceb` | unsure | 0.562 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `628e0650-a60a-47b8-a34c-11ccd1e03209` | human | 0.675 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `639a01ba-b6ee-457e-9558-3b2a6995133a` | unsure | 0.552 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `6556c9eb-64a3-4da1-9874-e0b231b8719b` | unsure | 0.511 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `fd1ebcc8-df03-42ad-8142-71fbd0f2990e` | unsure | 0.507 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `cf5d6bf3-8289-42e2-81fa-ede6b61aa5ee` | unsure | 0.536 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `ac833d54-962b-4884-9420-fc3993918c6a` | human | 0.700 |  |
| MF04 | malformed | text is only punctuation | 200 | `ed6e6b69-6a46-4f60-9e62-d9568d671a89` | human | 0.696 |  |
| MF05 | malformed | text is a very long single word | 200 | `e4024fff-ec79-46d9-a8b6-e0124bc1fca9` | ai | 0.699 |  |
| MF06 | malformed | text is emoji only | 200 | `a63c9526-fc29-4b9a-b91c-0da66bb3ba6a` | ai | 0.699 |  |
| MF07 | malformed | text is right-to-left script | 200 | `2f389316-2d68-4243-8106-9cdfaa22ec36` | ai | 0.663 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `8533d21c-51a6-4ed0-8994-5d7279368ca7` | ai | 0.790 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `54aa70ea-3597-4b26-9032-05369479f1f8` | human | 0.689 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3e345acb-1498-45fb-b5c0-cc3401a78f5c` | human | 0.689 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d85f8781-46f5-4abd-a08d-492b35421549` | human | 0.689 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d3b79421-24d1-4c47-a593-3efc4b09be61` | human | 0.689 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `be037dae-3015-4a5c-b317-e7006d610c94` | human | 0.689 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8714b2c2-31c5-46ba-9cb7-5315e041654e` | human | 0.689 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fd3d8ef9-a726-4735-974e-f48e09f6f801` | human | 0.689 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `493559e1-b989-4070-9bbf-5aca8e8369ed` | human | 0.689 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `d13a4429-5c48-435a-aa24-664658e0447b` | human | 0.689 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a2566dbe-eccb-47bb-9fa9-7bc4db30b027` | human | 0.689 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

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
