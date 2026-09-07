# Validation notes

These notes distinguish package installation from the behavior of an agent using the skill. Neither proves that every product, platform, or defect type has been tested.

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

Run `python3 scripts/validate.py` from the repository root. It checks matching plugin metadata, both catalog source paths, the shared skill entrypoint and resources, and local Markdown links. It requires only the Python standard library and does not execute product tests or validate third-party web pages.

Package checks performed on 2026-09-07:

| Check | Result |
| --- | --- |
| Standard-library repository validator, Python 3.9 | Passed |
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
