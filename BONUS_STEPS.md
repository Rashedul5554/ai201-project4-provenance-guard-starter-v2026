# Unit 7 — install all three bonus features

Do these steps in order. Do not copy the final README before committing the declaration.

## 1. Commit the declaration before installing the bonus code

Copy ONLY 01-declare/README.md into your Desktop project as README.md. Save it.
In your right VS Code terminal, run:

```bash
git add README.md
git commit -m "Declare all three Unit 7 bonuses before implementation"
git push origin main
```

This declaration must precede the implementation in repository history. Keep the
actual chronology; do not describe the prepared package as code you wrote unaided.

## 2. Install the implementation

Stop the server in the left terminal with Control+C.
Copy ALL files inside 02-implementation/ into the project root, replacing the
matching files. Include the hidden .gitignore file (Command+Shift+period in Finder
shows hidden files). Do not replace criteria.md, audit.py, detector.py, stylometry.py,
run_attacks.py, run_eval.py, or scenarios.py.

New files: provenance.py, verification.py, capture_bonus_evidence.py, BONUS_STEPS.md.
Updated files: app.py, scoring.py, config.py (weights only), README.md, .gitignore.

Restart the service in the left terminal:

```bash
python app.py
```

## 3. Complete the extra human-verification step

In the right terminal:

```bash
python verification.py request --creator rashedul
```

A reviewer needs to observe you read the displayed random phrase and compose a
short original paragraph live, in person or on a live call. This is a real extra
step, not something the AI assistant can do for you. Do not post confidential
workplace or patient information. The reviewer then operates the local command:

```bash
python verification.py approve --reviewer "ACTUAL REVIEWER NAME"
```

Replace ACTUAL REVIEWER NAME. Only after observing the live task should the
reviewer type OBSERVED. Requests expire in 30 minutes and cannot be reused.
The credential token is saved in .private/; do not commit or share that folder.
A self-approved simulation must be disclosed as a simulation and may not satisfy
the grader's verified-human requirement.

## 4. Capture real evidence and finish the README

With the server running, in the right terminal:

```bash
python capture_bonus_evidence.py
python test.py
git status --short
git check-ignore .private/writer_credential.json
```

The capture script does not issue a credential. It requires the reviewer's
completed step, performs requests against your running model, saves responses,
and updates the README's sample-run and bonus evidence blocks. It omits token
secrets from public evidence. Review the generated README before submitting.
If it reports a missing label, keep the result and resolve label reachability
before claiming all three categories have appeared under the new weights.
The environment check is not a full acceptance-criteria evaluation.

## 5. Commit the implementation and evidence

```bash
git add app.py scoring.py config.py provenance.py verification.py capture_bonus_evidence.py BONUS_STEPS.md README.md .gitignore results/ logs/audit.jsonl
git commit -m "Implement three Unit 7 bonuses and record local evidence"
git push origin main
```

Unit 8 rate limiting and evaluation scripts remain unchanged. Original criteria
and their history remain unchanged. The original AI-assisted criteria authorship
issue is not resolved by these bonus features; consult your instructor and keep
the disclosure accurate. No score is guaranteed until graded.
