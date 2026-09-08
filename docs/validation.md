# Validation notes

These notes distinguish package installation from the behavior of an agent using the skill. Neither proves that every product, platform, or defect type has been tested.

## 1.1.0 validation

The entrypoint now starts with product artifacts and uses reference sections only for unresolved questions. It was reduced from 1,177 to 718 whitespace-delimited words; this is a document-size measure, not a measured model-token saving. The optional native-command helper preserves complete attempt logs and returns a bounded output tail without interpreting test success. Planning templates now start at NOT RUN.

The previous small and integrated synthetic comparisons did not demonstrate a detection advantage over ordinary model QA. In the Luna integrated comparison, the old skill used more average time and tokens; removing an ambiguously scoped concurrency item made detection equal. These observations motivated the redesign and do not establish the new version's performance.

New validation uses a frozen skill and real historical Tornado defects selected from BugsInPy, with full source snapshots and independent buggy/fixed controls. The comparison includes no skill, a fixed short QA prompt, and the revised skill. This is a small adapted subset with one project, not the full official BugsInPy benchmark, and public-code training exposure cannot be ruled out. Reproducible setup is kept separately from the installed skill payload.

The completed Luna screening did not show a quality advantage: all three conditions observed one of three selected defect families; no-skill additionally found one real decoding defect. False product findings were 2 / 1 / 2 for no-skill / short-prompt / revised-skill. Revised skill took 2.68% more total time and 3.49% fewer input+output tokens than no-skill, but 19.98% more time and 17.10% more tokens than the short prompt. These are one-run-per-task observations, not statistical proof. Exact measurements, independent oracle adjudication, condition contamination and excluded costs are in the [public-project screening report](evaluation-2026-09-08.md).

On macOS ARM / CPython 3.9.6, nine helper behavior tests cover literal arguments, real exit codes, bounded output with full log retention, preserving initial failures, setup errors, timeouts and process-group cleanup. Ten package tests exercise valid and malformed YAML, required field types, and missing links. Windows process-tree cleanup remains best effort and has not been executed on Windows.

All 19 package/helper tests and both native manifest validators passed for 1.1.0. The shared, standalone and ZIP skill payloads match the 19 frozen files. The public environment builder was independently replayed, with nine expected native unittest outcomes and source-integrity checks passing. During model comparison no revised run invoked the optional helper, so the study does not establish its efficiency benefit.

## Behavioral exercises

During development, separate evaluation agents received the skill, a task, and source materials without being told the seeded defects or expected conclusions. The exercises ran in isolated local fixtures, not against production services.

| Exercise | Observed result | Behavior checked |
| --- | --- | --- |
| Ticket quotation function | 83 input cases: 53 passed, 30 failed; failures consolidated into three seeded product defects | Actual execution, independent expectations, boundaries, discount decision rules, and defect deduplication |
| Mobile inspection application, planning only | 11 risks, 24 case families, 12 unresolved policy questions; no product execution | Offline data, permissions, immutable approvals, synchronization races, byte boundaries, and preserving uncertain requirements |
| RAG release evidence packet | Insufficient release evidence despite a reported 96/100 success count | Candidate mismatch, self-grading, contaminated holdout data, blocked authorization checks, and average-latency limitations |
| Small pagination helper | Standard-library unittest: eight methods, 29 input cases; 23 passed, six failed, one seeded rounding defect | Proportionate testing with an ordinary runner and clear distinction between methods and input cases |

These are development observations, not a standardized benchmark or a claim that the skill itself had 36 failing tests. Failures above are deliberately faulty fixture behavior.

The first three exercises informed refinements to avoid unnecessary reporting harnesses and to separate oracle certainty from execution status. The pagination exercise checked the simpler execution approach. The final wording and templates received structural review; the entire behavioral suite was not rerun after every wording change. The fixtures and agent transcripts are not included in this public package, so this table is a development summary rather than a reproducible benchmark.

## Package checks

From the repository root, install the development-only dependencies with `python3 -m pip install -r requirements-dev.txt`, then run `python3 scripts/validate.py` and `python3 -m unittest discover -s tests -v`. The checker parses the skill/UI YAML, checks matching plugin metadata, both catalog source paths and local Markdown links. These dependencies are not required to install or use the skill. Package checks do not execute product tests or validate third-party web pages.

Package checks performed on 2026-09-07:

| Check | Result |
| --- | --- |
| Original standard-library repository validator, Python 3.9 | Passed at the time; later negative controls exposed incomplete YAML validation, corrected in 1.1.0 |
| Codex bundled skill and plugin validators | Passed |
| Claude Code 2.1.227 marketplace validation | Passed |
| Claude Code 2.1.227 plugin validation | Passed |
| Shared skill compared with the validated standalone distribution | All 18 files identical |
| GitHub Actions package validation on the public repository | Passed |
| Codex CLI 0.144.5: add GitHub marketplace, install plugin, list enabled plugin | Passed, version 1.0.0 |
| Codex app-server: reload and list skills | Discovered enabled plugin skill `lazyest-qa:lazyest-qa` from the plugin cache |
| Claude Code 2.1.227: add GitHub marketplace, install, inspect details | Passed, version 1.0.0; component inventory found one skill named `lazyest-qa` |
| Codex standalone GitHub skill installer with an isolated destination | Passed; all 18 installed files identical to the source |
| Native plugin cache contents in Codex and Claude Code | Shared skill files identical to the source |
| GitHub source archive fetched without authentication | Downloaded successfully; every plugin payload file matched the local source |

Native installations above used `lazyest-hyun/lazyest-qa` on GitHub, not a local directory. They verified fetching, installation, enabled state, and skill discovery. They did not start a paid model session or rerun the behavioral exercises in both hosts. The Codex app UI was not part of this CLI validation.

The package uses one shared skill directory; native tool support and the user's available execution tools determine which tests can actually run.

## Scope of evidence

The exercises did not execute real mobile devices, production servers, external AI models, load generators, hardware rigs, or regulated validation programs. Those require suitable environments and domain evidence in the actual assignment. A successful plugin installation confirms delivery and discovery of the skill, not the quality of every future test result.
