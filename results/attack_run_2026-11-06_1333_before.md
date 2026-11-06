# Attack run — before

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-06 13:33
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `d30ed0c3-bada-4a5b-b647-c7ca150474ab` | unsure | 0.584 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `cf20b642-f82c-47bf-b4c6-137ac9d4df88` | unsure | 0.546 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4bd5e3a6-91fd-4bef-b835-08d8dfc4a5f0` | unsure | 0.557 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `149fd8dc-4dc2-45ae-bb12-39ed90175b85` | unsure | 0.591 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `041bf2a2-7f9b-4a24-9a8e-2eaf04ce3ac0` | unsure | 0.618 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `27f3fb31-7656-4069-80c9-b6ec690ba852` | unsure | 0.573 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `401162e7-d32c-4b08-a9cc-63c609516b6e` | unsure | 0.534 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `1b60c206-fe72-4ae7-adc6-8baa19fbdbfb` | unsure | 0.602 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c54702a8-c39d-4d4b-bba5-804c4182046f` | unsure | 0.570 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0fc03469-effc-4f17-8575-50896e02554a` | ai | 0.780 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `3b2c034d-a580-46d6-9ac3-37c4a36e949d` | unsure | 0.557 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `e70c72b0-ec4f-4d0a-a9c3-b7e8c222d108` | unsure | 0.650 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `e5c2e836-5c8e-427a-be8c-e0c5cf9a8e30` | ai | 0.658 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `242b6f90-db2d-45dd-886f-5d4471aedfe6` | unsure | 0.648 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `d1e895ab-d428-4913-9e1e-5b0c9031c74b` | ai | 0.676 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `70ab6cde-b6f4-48a5-888b-b12a971469fd` | ai | 0.650 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c1b0dc2c-9cd1-4bd4-80eb-0f435ece75bf` | unsure | 0.636 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `9e8482e4-b3b0-4da9-9957-828c55f72f9a` | unsure | 0.571 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `24dee286-de06-4c5e-928e-980571ce89a9` | unsure | 0.562 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `59bb5238-89d2-452d-92b2-d0518444b299` | human | 0.675 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `490e3282-9dad-4388-a52c-3db29c8702b5` | unsure | 0.552 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `4752a28f-d996-4adc-91bf-c9cc9a232779` | unsure | 0.511 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `f62df00c-a9c5-401a-8bfd-e4c9a6d9f969` | unsure | 0.507 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `b1b04531-32f1-47b9-b4b8-37b4dab52ae8` | unsure | 0.536 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `f2138593-92b9-46ee-9452-2e708f220300` | human | 0.700 |  |
| MF04 | malformed | text is only punctuation | 200 | `991138de-7e5b-4e29-8fed-7fbb648778dc` | human | 0.696 |  |
| MF05 | malformed | text is a very long single word | 200 | `d98608f8-c672-4f44-9fe6-fff412e7979a` | ai | 0.699 |  |
| MF06 | malformed | text is emoji only | 200 | `c3f72bfd-c517-4e20-abf2-9fcb221f8ae2` | ai | 0.699 |  |
| MF07 | malformed | text is right-to-left script | 200 | `c1632489-ce20-4796-a241-30009fa570bf` | ai | 0.663 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `baf280b9-0f7e-4564-b485-1670e9047236` | ai | 0.790 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `4e802c60-61aa-4d31-841b-17cbf669772c` | human | 0.689 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `bd6fc1ae-5c59-493f-908b-98d37871c123` | human | 0.689 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `72931f07-f601-4365-84d8-4d5d4d221e8a` | human | 0.689 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e1f05ddb-b2ae-4bf7-b94e-ce55c6b827fa` | human | 0.689 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `af7fdbf7-d84f-4487-9bad-c683d5d69518` | human | 0.689 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `38ecb97f-b5e1-4ae8-af0e-0f049d709055` | human | 0.689 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2bc7ae77-1649-469c-9f3f-ba89555aa7c7` | human | 0.689 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3962abf2-191e-431a-8fe0-c73d17039f61` | human | 0.689 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2daeec43-9258-4af2-b5d6-0946bc6f4c7e` | human | 0.689 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c0164f76-4337-407d-a753-8f68b877f153` | human | 0.689 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 200 | `130973f2-e273-4fe3-94ce-3cb5c71ecdbc` | human | 0.689 |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 200 | `fbeff827-de50-4c1f-9a6e-9ad5eed436e3` | human | 0.689 |  |

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
  "content_id": "d30ed0c3-bada-4a5b-b647-c7ca150474ab",
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
  "content_id": "cf20b642-f82c-47bf-b4c6-137ac9d4df88",
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
  "content_id": "4bd5e3a6-91fd-4bef-b835-08d8dfc4a5f0",
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
  "content_id": "149fd8dc-4dc2-45ae-bb12-39ed90175b85",
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
  "content_id": "041bf2a2-7f9b-4a24-9a8e-2eaf04ce3ac0",
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
  "content_id": "27f3fb31-7656-4069-80c9-b6ec690ba852",
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
  "content_id": "401162e7-d32c-4b08-a9cc-63c609516b6e",
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
  "content_id": "1b60c206-fe72-4ae7-adc6-8baa19fbdbfb",
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
  "content_id": "c54702a8-c39d-4d4b-bba5-804c4182046f",
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
  "content_id": "0fc03469-effc-4f17-8575-50896e02554a",
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
  "content_id": "3b2c034d-a580-46d6-9ac3-37c4a36e949d",
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
  "content_id": "e70c72b0-ec4f-4d0a-a9c3-b7e8c222d108",
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
  "content_id": "e5c2e836-5c8e-427a-be8c-e0c5cf9a8e30",
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
  "content_id": "242b6f90-db2d-45dd-886f-5d4471aedfe6",
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
  "content_id": "d1e895ab-d428-4913-9e1e-5b0c9031c74b",
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
  "content_id": "70ab6cde-b6f4-48a5-888b-b12a971469fd",
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
  "content_id": "c1b0dc2c-9cd1-4bd4-80eb-0f435ece75bf",
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
  "content_id": "9e8482e4-b3b0-4da9-9957-828c55f72f9a",
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
  "content_id": "24dee286-de06-4c5e-928e-980571ce89a9",
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
  "content_id": "59bb5238-89d2-452d-92b2-d0518444b299",
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
  "content_id": "490e3282-9dad-4388-a52c-3db29c8702b5",
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
  "content_id": "4752a28f-d996-4adc-91bf-c9cc9a232779",
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
  "content_id": "f62df00c-a9c5-401a-8bfd-e4c9a6d9f969",
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
  "content_id": "b1b04531-32f1-47b9-b4b8-37b4dab52ae8",
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
  "content_id": "f2138593-92b9-46ee-9452-2e708f220300",
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
  "content_id": "991138de-7e5b-4e29-8fed-7fbb648778dc",
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
  "content_id": "d98608f8-c672-4f44-9fe6-fff412e7979a",
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
  "content_id": "c3f72bfd-c517-4e20-abf2-9fcb221f8ae2",
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
  "content_id": "c1632489-ce20-4796-a241-30009fa570bf",
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
  "content_id": "baf280b9-0f7e-4564-b485-1670e9047236",
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
  "content_id": "4e802c60-61aa-4d31-841b-17cbf669772c",
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
  "content_id": "bd6fc1ae-5c59-493f-908b-98d37871c123",
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
  "content_id": "72931f07-f601-4365-84d8-4d5d4d221e8a",
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
  "content_id": "e1f05ddb-b2ae-4bf7-b94e-ce55c6b827fa",
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
  "content_id": "af7fdbf7-d84f-4487-9bad-c683d5d69518",
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
  "content_id": "38ecb97f-b5e1-4ae8-af0e-0f049d709055",
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
  "content_id": "2bc7ae77-1649-469c-9f3f-ba89555aa7c7",
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
  "content_id": "3962abf2-191e-431a-8fe0-c73d17039f61",
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
  "content_id": "2daeec43-9258-4af2-b5d6-0946bc6f4c7e",
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
  "content_id": "c0164f76-4337-407d-a753-8f68b877f153",
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
  "status": 200,
  "content_id": "130973f2-e273-4fe3-94ce-3cb5c71ecdbc",
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

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 200,
  "content_id": "fbeff827-de50-4c1f-9a6e-9ad5eed436e3",
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
