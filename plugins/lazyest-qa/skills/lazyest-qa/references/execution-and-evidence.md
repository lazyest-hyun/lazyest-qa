# Execute and preserve evidence

Read before dynamic testing. Use actual host capabilities; do not invent tools, visible UI, credentials or network access.

## Preflight

1. Identify intended target from context and observed configuration: local/test/staging/production, build/commit and flags. A hostname alone does not establish safety.
2. Inspect runner commands and setup/teardown hooks. A command named `test` can migrate a shared database, call a paid API or delete data.
3. Prefer isolated environments and synthetic or approved data. Discover dependencies before installing replacements; follow the package manager and lockfile.
4. For shared writes, realistic load, failure injection, paid calls or irreversible effects, check existing authority and limits. If missing, prepare exact target/action/limit and ask only for missing authority; continue authorized checks. Ordinary local tests need no new approval ceremony.
5. Run one useful viability case before an expensive suite. Define timeouts and cleanup of owned resources.

Do not automatically deploy, restart shared services, reset shared databases, change credentials or send notifications to enable testing. An explicit assignment may authorize these; this skill does not.

## Execute behavior

- Reuse repository runners/CLI, authorized APIs, available browser/native automation, or supplied reports as appropriate. If only human execution is available, give precise cases and label them not run by the agent.
- Isolate users/tenants, IDs and fixture state; control time/randomness where appropriate. Remove only owned test data.
- Assert meaningful effects. Async acceptance and business completion are separate checkpoints. Correlate operation IDs and poll a condition with bounded timeout; arbitrary sleep is weak synchronization.
- Capture response, stored state, event count, visible state or downstream receipt as needed to prove the assertion, avoiding unnecessary private data.
- Parallelize only independent cases. For races, use barriers or synchronization to exercise the critical interleaving; a parallel loop may miss it.
- Record candidate/environment/configuration/data differences when comparing a baseline.

## Evidence record

Keep: `case/scenario ID; basis/risk; candidate/build; environment/client; timestamp; setup/data/seed; command or actions; expected; actual; status; artifact; cleanup`.

Shared run metadata can cover multiple cases. Native runner output plus concise notes is sufficient for small tests; do not build a reporting framework merely to fill these fields. Record relevant environment versions, not unnecessary host identity or full environment dumps. Use portable artifact references in shared reports.

For automated runs record exact command and working context, summary/exit, selected/collected/executed/skipped counts when available, and log or concise output. Exit zero with zero collected tests is not a passing suite. Builds and type checks support their own claims, not behavioral execution claims.

For UI runs record route/state, role, client and interaction evidence. A screenshot proves visible state at a point in time, not persistence, keyboard access, network behavior or another device.

Preserve original failures and reruns with secrets/personal data minimized. Link evidence to the candidate; subsequent code/environment changes can invalidate it. Keep baseline and candidate records separate.

## Outcome semantics

| Status | Meaning |
| --- | --- |
| PASS | Executed observations meet defined expectations in the recorded environment |
| FAIL | Confirmed execution mismatch with an established expectation |
| BLOCKED | Missing prerequisite prevented execution/completion; identify it |
| NOT RUN | Planned/selected work has not been attempted |
| INCONCLUSIVE | Missing oracle, contaminated run or inadequate sample prevents a verdict |
| SKIPPED | Deliberately omitted, with reason and scope impact |
| NOT APPLICABLE | Condition does not apply, with justification |

Map to project labels without losing distinctions. Preserve a runner's raw failure status while separately classifying environmental causes. Flakiness is an additional finding with attempt history; a pass-on-retry is not a clean pass.

## Investigate

Preserve trigger, data, timing and state. Minimize reproduction; compare against the basis. Check test/setup and target identity before attributing product cause. Separate observation from root-cause inference.

Correct an erroneous test only after explaining the wrong oracle/setup. If product fixes are authorized, reproduce before fixing where practical, then rerun the original case and affected regression. Otherwise report the defect without product changes.

Reruns investigate intermittency/environment, not erase failure. Retain attempt counts/results and stop when another run adds no evidence. Quarantine needs a reason, owner and restoration criterion and leaves a visible coverage gap.

## Cleanup and handoff

Clean owned resources when permitted and verify important cleanup effects. Report leftovers without destroying reproduction evidence. Finish with results, residual gaps and next action; do not claim blanket success from a subset.
