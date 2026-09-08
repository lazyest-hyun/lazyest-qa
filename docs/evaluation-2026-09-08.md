# Public-project QA screening, 2026-09-08

This is a three-task, single-project screening of revised Lazyest-qa, not a full benchmark score or evidence of universal performance. The three historical Tornado tasks and buggy/fixed controls can be rebuilt with the [public environment scripts](../benchmarks/public-qa/README.md).

## Conditions and measurement

GPT-5.6 Luna / medium, Codex CLI 0.144.5, CPython 3.9.6, macOS ARM. Each task ran once under no skill, a short QA prompt, and the frozen revised skill. Conditions used the same tools and a six-minute assignment with a seven-minute hard ceiling. Sequential order rotated no/short/skill, short/skill/no, skill/no/short. The entrypoint and all 19 skill files were frozen before the skill author read the new gold tests or patches. This study did not directly compare v1 and v2 on the same tasks.

Participants received full buggy source without Git history or hidden gold tests. They were instructed to write and execute tests, preserve actual logs, and produce a concise Korean report in their own result folder. Native runners, local test doubles, temporary synthetic data, synchronization and loopback servers were allowed. Source modifications, installations, outside services, answer searches, other runs, memory, outside QA skills and delegation were prohibited. The installed standalone QA skill was disabled in every invocation; only the revised condition received the frozen skill path. Native Codex instructions remained present in every condition.

Exposed command traces and input hashes were audited. This was not an OS-enforced read boundary or proof of training-data novelty. Copying materialized three legacy App Engine maintenance symlinks identically across conditions in tasks B/C; the tested `tornado` package bytes were unchanged. Public preparation scripts preserve the original archive topology.

The short condition added this fixed guidance to the common task:

> Inspect the actual requirements, relevant source and existing tests. Prioritize material risks from the change and its dependencies. Design concrete tests with independent expected results, including meaningful state sequences, boundary interactions and supported integration behavior where relevant. Reuse native runners and fixtures; run focused checks and preserve actual failures. Distinguish product defects from incorrect tests, setup problems and unresolved requirements. Verify observable effects rather than relying on a successful status or a code explanation alone. Revisit important uncovered risks before finishing. Give a concise report of confirmed findings, reproduction steps and material untested areas. Do not claim that planned or blocked checks passed. Use only the approved local resources and do not fix application code.

Time includes instruction reading, navigation, test writing, tool calls, corrections and reporting from native process start to exit. Environment setup and independent grading are excluded. Tokens are actual native usage, accumulated across requests; cached input is a subset of input, and reasoning output is a subset of output. Neither is added twice. These are not unique-document token counts, dollars or account-quota percentages. Cache state and service scheduling were uncontrolled.

## Results

The revised skill did **not** demonstrate a quality advantage. Independent graders replayed unedited submitted tests against buggy and fixed snapshots, then checked the behavioral oracle separately. A real defect outside the selected gold family was adjudicated with a separate evaluator-only one-line correction; failure on the historical gold revision was not automatically treated as a false positive.

| Condition | Selected defect families observed, of 3 | Additional real defects | False product findings |
|---|---:|---:|---:|
| No skill | 1 | 1 | 2 |
| Short QA prompt | 1 | 0 | 1 |
| Revised skill | 1 | 0 | 2 |

All conditions observed the static-file Range boundary failure, but their regression expectations included unsupported HTTP status assumptions. Therefore observing this defect family is not equivalent to producing a wholly correct regression suite. All missed the loop-retention family and the low-level HTTP/1.0 keep-alive family. The no-skill condition additionally found that `Transfer-Encoding: Chunked` was not decoded; the same unedited test passed after an isolated case-normalization correction in an evaluator copy.

The loop task exposed an unsupported assumption that a closed current loop must automatically become a new open loop. All conditions reported this as a defect although the submitted tests also failed on the fixed control and the existing contract did not support that expectation. In the HTTP task all conditions used a client configuration that bypassed the selected defective branch. Executed passing tests did not establish that branch's coverage.

Reporting errors were also retained separately: revised task A misstated a HEAD response, used a 65,281-byte fixture while claiming 65,535, and claimed range coverage after an earlier assertion had stopped the loop. Short task A miscounted method passes by treating two subtest failures as two failed methods. Revised task C incorrectly described a 204 response with `Content-Length: 0` as valid; that was an input-validity interpretation error, not an additional product false positive.

The first preserved confirmed static-file defect symptoms appeared at 76.509 / 79.227 / 92.337 seconds for no/short/revised. No condition produced valid loop-retention or selected HTTP defect evidence. The additional no-skill HTTP defect appeared at 92.554 seconds. These timestamps belong to the test version actually executed then, not necessarily the submitted final file. A failed assertion alone was not accepted; the observed product symptom needed independent confirmation.

Oracle sources: [RFC 7233 sections 2.1 and 3.1](https://www.rfc-editor.org/rfc/rfc7233.html), [RFC 7230 sections 3.3.2 and 4](https://www.rfc-editor.org/rfc/rfc7230.html). [Compact adjudication JSON](evaluation-2026-09-08-quality.json) records the nine classifications independently of cost.

| Condition | Mean total seconds | Total input | Cached input, included | Uncached input | Output | Total input + output |
|---|---:|---:|---:|---:|---:|---:|
| No skill | 155.067 | 1,731,716 | 1,592,320 | 139,396 | 19,857 | 1,751,573 |
| Short QA prompt | 132.708 | 1,425,185 | 1,292,288 | 132,897 | 18,447 | 1,443,632 |
| Revised skill | 159.224 | 1,668,864 | 1,526,272 | 142,592 | 21,622 | 1,690,486 |

Totals cover three tasks per condition. [Per-run CSV](evaluation-2026-09-08.csv) retains the nine time/token records. Relative to no skill, the revised condition took 2.68% more time and 3.49% fewer input+output tokens, while uncached input rose 2.29% and output rose 8.89%. Relative to the short prompt, it took 19.98% more time and 17.10% more input+output tokens. These small-sample differences do not establish causal or statistical superiority.

All revised runs read the exact frozen entrypoint once. They read no optional references and never executed `run_check.py`. Consequently the helper's logging behavior was unit-tested, but its effect on model efficiency was not measured here. Shortening the entrypoint reduced its size; it did not establish the requested combination of better QA, faster completion and fewer tokens.

## Excluded attempts and limits

An initial revised condition read the globally installed v1 instead of the supplied v2. After detecting this from the actual command output, the entire initial set was excluded and all nine conditions restarted with the same per-invocation installed-skill disablement. No global settings changed. The frozen revised payload was not tuned to these results.

Four completed excluded runs consumed 671.707 seconds, 2,493,243 input tokens (2,298,624 cached) and 30,541 output tokens. A separate isolation check used 29,708 input (23,040 cached) and 309 output tokens. One interrupted attempt returned no final usage, so its consumption is unknown, not zero. These excluded costs are separate from the table and do not include preparation, grading or other agent work. Full transcripts and grading evidence are retained in the development workspace; this public repository includes compact measurements and environment reconstruction, not those private-path traces.

NocoDB/Defects4REST preflight was incomplete and excluded before the measured comparison. The study covers selected modules of one historical Python project, not REST applications, mobile devices, browser QA, load testing, or every skill route. Public upstream code may have appeared in training. Future changes need independently held-out tasks; adding these exact answers to the skill and retesting them would not show generalization.
