# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-07 23:00
- Auto-marked BROKE (5xx, crash, no response): **0**
- Reviewed verdicts: **42 HELD / 14 BROKE**
- Unjudged rows: **0**

The same rules as the reviewed baseline were applied. FP03, FP05 and FP06
moved from BROKE to HELD because their labels changed from ai to unsure.
MF07 also moved to unsure and remains HELD under the valid Arabic-input
robustness rule. The remaining 52 HTTP/guess outcomes matched the baseline.
The runner's raw JSON is preserved, including its original verdict fields.

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

---

## By family

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion | 10 | 1 | 9 |
| false_positive | 8 | 8 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| malformed | 20 | 16 | 4 |
| prompt_injection | 6 | 5 | 1 |

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "220c7112-89c7-4044-bd66-30ab2820c388",
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
  "content_id": "d9ed5be8-46c8-4db6-aaf1-c4424d4e02fa",
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
  "content_id": "9c1473e1-aa3d-4589-a13b-ce03d8195ba3",
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
  "content_id": "e31b3dbf-7f7f-4901-866c-50ec9124f603",
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
  "content_id": "4cf3efc4-dd50-4f8b-957a-98cf3c38ddbc",
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
  "content_id": "cf19401e-916a-48d3-83c0-8d12da7f749f",
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
  "content_id": "a5a586db-ce02-4eee-8d5b-7ddfaa4ad35d",
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
  "content_id": "623f7422-a988-4c38-8041-c7babe1b2b81",
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
  "content_id": "0635537a-2ab4-407c-b6fa-d43dcb0d786a",
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
  "content_id": "c552ebbf-caa2-4103-9cda-07e3f859b1ad",
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
  "content_id": "3290e1bc-8873-46d3-b000-7e7269f7c015",
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
  "content_id": "8a9aa68b-259b-4e4a-a680-b4ad1a3d9273",
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
  "content_id": "3e78f46f-914c-40b7-93bc-1b97feea7cf1",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.6578,
  "model_score": 0.8051,
  "style_score": 0.5895,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
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
  "content_id": "7332ae5b-dee5-4916-a830-dab2b61449ad",
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
  "content_id": "9abd28b8-e24e-4426-8125-22e3441bcd71",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.6764,
  "model_score": 0.8005,
  "style_score": 0.6406,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
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
  "content_id": "2cf3fc24-ef67-43a3-a3bf-fb3bdfaed0df",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.6503,
  "model_score": 0.8814,
  "style_score": 0.4944,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
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
  "content_id": "b7f31722-039f-4c3b-b398-d3e2d665876c",
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
  "content_id": "3fa4af24-9acb-4c5f-8267-66d6190f77cf",
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
  "content_id": "a4aaa15b-9a28-4093-8dda-059d5e54e5b0",
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
  "content_id": "34656792-deff-4c21-8713-07ae864796fc",
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
  "content_id": "ff3a7493-266e-4d83-bb3a-60cdde85cafc",
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
  "content_id": "f2c03161-3e83-4e2d-8273-4f7775a49409",
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
  "content_id": "06b49196-ffc9-4f0e-8125-9dbc6d90f69e",
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
  "content_id": "d9e37cb8-da99-4a42-8688-276240f28907",
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
  "content_id": "f5953ce5-162f-44cc-a04a-ceccddb2027c",
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
  "content_id": "455e1fb8-abd7-4a77-b86f-c735bb0bdf2e",
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
  "content_id": "e74698b9-0ea1-403f-aae6-6c33dd26615e",
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
  "content_id": "2c505972-d18d-4156-8d53-51a76bf87d0d",
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
  "content_id": "3bf61ad1-b771-49c4-8a6c-43f1e2f0d4dd",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.6626,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We cannot reliably tell whether AI was involved in this writing. This is not a finding of wrongdoing. The writer can request a review.",
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
  "content_id": "9bc0fcb3-bc5b-4a9a-aa6b-94376860965f",
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
  "content_id": "b25e11d6-d859-4fe0-b437-b27dd34cef96",
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
  "content_id": "88615031-4b9c-4bb6-a92b-0bfaafc5bafe",
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
  "content_id": "1c7e2f47-a75b-43cc-a443-23af995cff67",
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
  "content_id": "c8d565c9-dc34-40fa-b761-980f58daa2ee",
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
  "content_id": "45e17a5a-d3d5-4438-a630-0987a768ee18",
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
  "content_id": "92350073-70f9-454e-be78-ce5b2df34e6e",
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
  "content_id": "0c41d930-9d04-4c82-a6cd-479892969d58",
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
  "content_id": "05725fab-b2b5-4e0a-bd9b-509af2e3bc3f",
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
  "content_id": "6a71d279-27e0-4c9e-98a2-1984f2314709",
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
  "content_id": "e1325d60-89bf-4857-bb79-5017f30db43c",
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
