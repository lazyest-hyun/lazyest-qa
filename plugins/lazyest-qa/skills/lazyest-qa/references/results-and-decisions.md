# Results, defects and decisions

Use for progress, completion, defect verification and release readiness. Preserve [execution status semantics](execution-and-evidence.md). Reporting examples are adaptable conventions, not mandated ISTQB schemas.

## Trace evidence rather than test count

For substantial work link `basis/risk -> coverage item -> case -> run/environment -> result -> defect`. This can be a short table or existing tracker links; no new management system is required. Note uncovered important risks even if every selected case passes.

Distinguish:

- **Designed coverage:** identified items have cases; they may not have been run.
- **Executed coverage:** identified items were exercised; failures still exercise them.
- **Satisfied criteria:** evidence met the relevant expectation; a failed executed case is not satisfied coverage.

State the item set and denominator for any percentage. Execution rate uses the named selected applicable case set, with blocked/not-run/skipped visible. Pass rate among conclusive cases can use `PASS / (PASS + FAIL)` but must show the other statuses; it is not release confidence. State coverage, branch coverage and requirement coverage measure different sets. Zero denominator means unavailable/not applicable, not 100%.

Count unique case/configuration instances consistently; retries are attempts, not new coverage. If the runner reports only aggregate counts, report those instead of fabricating case-level traceability. Do not combine results across different candidates into one passing release suite without explaining relevance.

## Write a reproducible defect

Use [defect template](../assets/defect-report.md) where needed. Include:

- Concrete title: condition and wrong behavior.
- Basis and expected behavior, observed result and user/system impact.
- Candidate/environment, prerequisites/data, minimal steps or exact command, frequency/attempts.
- Evidence reference and scope/affected users; root cause labeled confirmed or suspected.
- Suggested next action and confirmation/regression scope.

Separate severity (impact) from priority (when to address). Use the project's scale. If missing, propose plain-language impact levels rather than treating a numeric scale as universal. A cosmetic issue can be urgent for a particular launch; a rare integrity issue can have severe impact. Do not downgrade harm merely because reproduction is difficult.

Triage findings as confirmed defect, likely defect requiring evidence, environment/test issue, requirement question, or improvement suggestion. Avoid presenting speculative causes as confirmed bugs. Link duplicates only when evidence establishes the same issue. External issue creation/commenting requires task authority; drafting a report does not.

## Release recommendation

Lead with a recommendation limited to the named candidate and assessed scope. Assess agreed exit criteria, critical workflows, unresolved defects, blocked/unrun checks and material environment gaps.

| Evidence state | Recommendation language |
| --- | --- |
| Relevant agreed criteria met, no unacceptable open risks | Ready for the assessed scope, with named limits and acceptance authority |
| Confirmed defect or unmet criterion exceeds accepted risk | Not ready; identify the specific blocker and verification needed |
| Critical evidence/oracle missing, no adequately supported verdict | Insufficient evidence; name the missing check/decision |
| Criteria met only under an accepted exception | Conditional recommendation with explicit exception, owner and follow-up |

Do not invent an exception acceptance, waive a failed gate, or say conditional-ready merely to avoid reporting a blocker. If criteria were never agreed, report findings against proposed criteria and the missing acceptance decision. A small patch QA task does not require a formal release verdict.

For report-only review, do not rerun tools or mutate the system unless authorized. Inspect provenance, version, sample, scope and contradictions. A developer's “tests passed” statement is weaker than an identifiable run with evidence.

## Verification and completion

Confirmation must target the original trigger on the corrected candidate. Regression selects other affected behavior; report them separately. A changed file or closed ticket does not establish either. If pre-fix execution is unavailable, explain the evidence used rather than claiming a red/green comparison.

Finish with outcome, tested scope/version, key findings, actual execution summary, meaningful gaps and next actions. Link detailed artifacts instead of flooding chat with every passing case. For plan-only work, explicitly say no tests were executed. For interrupted/blocked work, preserve reusable cases and exact remaining prerequisites.

For process feedback, identify a demonstrated source of escaped defects or waste, propose the smallest useful prevention measure and name how its effect could be observed. Do not turn every completed run into an obligatory process-redesign exercise.
