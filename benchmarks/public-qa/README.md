# Rebuild the public QA environment

This optional developer benchmark rebuilds three historical Tornado tasks from commits identified by BugsInPy. It measures executable QA against real defects, using the complete source repositories instead of synthetic functions. **Installing or using the QA skill does not require this benchmark, Python, Git, or any additional dependency.**

This folder distributes our preparation scripts, task descriptions, and commit metadata. It does not bundle Tornado source, BugsInPy framework code, gold tests, container data, credentials, or model run traces. Preparation reads source and gold tests from your existing local Tornado clone. It never downloads, installs packages, changes the clone's checkout, or removes an existing output path.

## Prepare and verify

Requirements: Python and Git supporting `--no-lazy-fetch` (verified with Git 2.50.1). The three tasks have been validated with **CPython 3.9.6 on macOS ARM64**, using only the standard library. Other Python versions, particularly newer asyncio implementations, may change these historical tests' behavior. Re-run verification in your environment before using the tasks. The tests open loopback sockets; they do not need an external service.

From the root of this skill repository:

```sh
# One-time download. Use gh's already authenticated account.
gh repo clone tornadoweb/tornado /tmp/lazyest-qa-tornado-source

# Both output directories must be new. Choose other paths for subsequent runs.
python3 -B benchmarks/public-qa/prepare.py \
  --repo /tmp/lazyest-qa-tornado-source \
  --out /tmp/lazyest-qa-tornado-benchmark

python3 -B benchmarks/public-qa/verify.py \
  --root /tmp/lazyest-qa-tornado-benchmark \
  --out /tmp/lazyest-qa-tornado-verification \
  --python /path/to/python3.9
```

Replace the last executable with your CPython 3.9 interpreter; `--python` defaults to the interpreter running `verify.py`. If a local clone already contains the six commits in `manifest.json` and all their source trees/blobs, preparation and verification work without network access. Shallow and partial clones may lack these objects: obtain a full clone before preparation. Git lazy fetching and transport protocols are disabled during preparation, and replacement objects cannot override pinned source. Missing commits fail before output creation; a missing historical blob can leave a partial new output directory. Nothing automatically fetches or deletes that directory; choose another new path after correcting the source clone.

`verify.py` runs nine native `python -m unittest -v ...` commands: an existing relevant module and the same upstream regression tests on both buggy and fixed snapshots for each task. The subprocess timeout defaults to 45 seconds and can be changed with `--timeout`. Its exit code is zero only when all expected outcomes and snapshot hashes match. JSON records include commands, working directories, runtime, elapsed time, test/failure/error/skip counts, log paths, and integrity checks; raw output is preserved in separate logs. A timeout or mismatching environment is a failed preflight, not evidence that a model detected a defect.

| Task | Existing relevant module | Expected upstream regression: buggy → fixed |
|---|---|---|
| Static content delivery | 182 tests, including 1 skip in the validated environment | 2 assertion failures → 2 passes |
| Event loop lifecycle | 6 passes | 2 assertion failures → 2 passes |
| HTTP client interoperability | 47 passes | 1 product error → 1 pass |

The HTTP task's expected error is the historical product's access to the nonexistent `ResponseStartLine.method` attribute. Verification checks this symptom, collected test count, and the fixed control. An arbitrary import error is not accepted as a reproduction. These are selected modules, not the whole project's test suite.

## Keep participant and evaluator files separate

```text
benchmark/
  cases/tornado-N/
    TASK.md             Participant task: no fixed SHA or gold-test names
    input/              Complete buggy git archive; no .git directory
    result/             Participant output directory
  evaluator-only/
    manifest.json       Fixed and buggy commits, exact gold-test selectors
    provenance.json     Source hashes and code size
    tornado-N/
      hashes.json
      gold/             Test file read from fixed commit with git show; LICENSE
      buggy/            Buggy source with the gold test file overlaid
      fixed/            Fixed source with that same test file
```

Provide each participant with only one `cases/tornado-N/` directory. The public helper directory itself contains answer metadata and must not be included in the participant workspace. A directory name is not an access boundary: place `evaluator-only/`, other runs, the original Git clone, and this helper checkout outside the participant's allowed filesystem. Disable outside-network answer search for the evaluation and audit tool traces. The original upstream LICENSE is retained in each snapshot and alongside gold tests.

Use independent copies for model-generated tests. Keep the prepared snapshots unchanged so the verifier can detect accidental source edits. Run a participant's submitted tests against both versions in separate grading copies. A useful detection must fail for the product defect on buggy source and pass on the fixed control; classify collection, dependency, fixture, and unrelated runtime failures separately. The upstream gold preflight here establishes a working environment; it does **not** grade model answers or measure a model's tokens.

For model comparisons, keep the model, reasoning effort, task, tools, timeout, and runtime identical across no-skill, short-QA-prompt, and skill conditions. Alternate condition order, retain failed runs, and record actual input/cached-input/output tokens plus total elapsed time and time to first valid reproduction. Do not add cached input to input tokens a second time. Keep preparation and grading costs separate from model execution. Do not score report length as QA quality.

## Scope and provenance

This is a **three-task, single-project, BugsInPy-derived subset**, not a full BugsInPy, SWT-Bench, or TestGenEval score. The tasks cover different historical revisions; they are not three simultaneous defects in one service. Full source sizes of roughly 40,000–46,000 Python lines increase repository navigation needs but do not prove each defect is difficult. Public defects may have appeared in model training. Removing local gold files prevents direct workspace leakage; it does not establish training-data novelty or eliminate memorization.

The commit IDs and dataset references are pinned in [manifest.json](manifest.json). [BugsInPy](https://github.com/soarsmu/BugsInPy/tree/11c5f1eea954a42132cfd06bf257766a7963e0fd) identifies the revisions; source and gold files are obtained directly from [Tornado](https://github.com/tornadoweb/tornado), whose snapshots carry Apache-2.0 licensing. Our helper scripts use this repository's MIT license. BugsInPy framework code is not redistributed or required. NocoDB/Defects4REST setup is not included because its buggy/fixed differential was not established in the local trial.
