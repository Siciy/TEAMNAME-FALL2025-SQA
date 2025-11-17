# Software Quality Assurance Report (Simplified)
## TEAM-FALL2025-SQA

Team: Thomas Brown, 
Deadline: Dec 01, 2025, 11:59 PM CST

---

## What we did (at a glance)

- Set up a clean GitHub repo for the project
- Wrote a fuzzing script (`fuzz.py`) that exercises 5 key functions
- Added practical logging (forensics) to 5 functions in `mining.py`
- Configured GitHub Actions to run fuzzing and lint checks automatically

---

## Scope of work

- Project: MLForensics (Python) — analyzing ML repos and scripts
- Files touched most:
  - `fuzz.py` (new)
  - `MLForensics/MLForensics-farzana/mining/mining.py` (logging added)
  - `.github/workflows/ci.yml` (CI config)

---

## Fuzzing (automatic tests)

Functions covered (5):
- `main.giveTimeStamp()`
- `mining.makeChunks(the_list, size_)`
- `mining.dumpContentIntoFile(strP, fileP)`
- `mining.deleteRepo(dirName, type_)`
- `mining.giveTimeStamp()`

How to run locally:
```bash
python fuzz.py
```

Result summary (local and CI): All tests passed (17 checks). The script writes a short summary to `fuzz_results.txt` when run locally. In CI, this file is uploaded as an artifact (not committed to the repo).

---

## Forensics logging (what and where)

Added logging to these functions in `mining.py`:
- `giveTimeStamp` — INFO/DEBUG around timestamp creation
- `deleteRepo` — INFO/WARNING/ERROR around directory deletion
- `dumpContentIntoFile` — INFO/DEBUG about file writes and sizes
- `makeChunks` — INFO/DEBUG about chunking
- `cloneRepo` — INFO/ERROR around git clone attempts

Logger configuration writes to console and `mining_forensics.log` when run locally. In CI, the log is captured and uploaded as an artifact. The repo ignores both generated files.

---

## Continuous Integration (GitHub Actions)

Workflow: `.github/workflows/ci.yml`

Runs on: push/PR to main/master/develop

Jobs:
1) Fuzzing tests — setup Python, install minimal deps, run `fuzz.py`, upload artifacts (fuzz results and log)
2) Code quality — run flake8 and pylint (non-blocking)

Where to find results: GitHub → Actions → select a run → download artifacts

---

## What we learned (short)

- Fuzzing is fast to add and catches edge cases (e.g., zero chunk sizes)
- Minimal, targeted logging provides a useful audit trail without noise
- CI keeps the repo clean and proofs changes on every push/PR

---

## How to grade quickly

1) View `fuzz.py` and `mining.py` changes  
2) Open Actions tab and download artifacts (fuzz results + forensics log)  
3) Run locally if desired:
```bash
python fuzz.py
```

Repo URL: https://github.com/Siciy/TEAMNAME-FALL2025-SQA

---

Prepared by: Kabro  
Date: November 17, 2025
