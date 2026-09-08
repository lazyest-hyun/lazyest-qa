---
name: lazyest-qa
description: Design and execute software tests, reproduce defects, verify fixes, and assess QA or release evidence. Use for exploratory QA, regression, test automation, and requirements reviews across software products. Adapt to existing project tools and approved behavior.
---

# Lazyest-qa

Use the supplied product, change, requirements and existing tests first. Apply the core below directly. Open a reference only to answer a specific question those artifacts leave unresolved; the reference list is not a reading checklist.

## Core

1. **Choose the result.** Plan/review requests produce cases or findings without executing or changing the product. Execution requests produce runnable checks and observed results. Fix verification needs the original trigger and affected regression. Release review needs evidence for the actual candidate. Preserve the user's scope and existing authorization.
2. **Find the shortest useful path.** Inspect the relevant contract, changed behavior, callers and existing test setup. Reuse the project's runner, fixtures and public interfaces. Read targeted files or sections; expand when dependencies or failures justify it. Execute a small relevant check before writing a large suite.
3. **Make risks executable.** For each material risk, identify the required outcome, setup/sequence, observation and a control that distinguishes correct behavior. Select probes that add distinct evidence; avoid repeating checks already sufficient for the same risk. Use the following prompts where the product exposes that mechanism:

| Mechanism | Discriminating probe |
| --- | --- |
| Limits or interacting rules | Adjacent valid/invalid values; isolate invalid inputs, then exercise relevant rule interactions |
| Stateful behavior | Establish state, perform another operation or change context, then reuse the resource; check effects as well as the response |
| Concurrent or asynchronous work | Identify conflicting transitions and an invariant; control their ordering with a local test barrier or clock when authorized; observe durable state after completion |
| Persistence, upgrade or encoding | Use nonempty historical data and meaningful round trips; compare identity, order, content and relationships |
| Multiple components or clients | Follow the contract across the actual boundary; retain the distinction between component simulation and observed integration |

4. **Execute and diagnose.** Tests must assert agreed behavior, not reproduce the implementation's formula. Keep raw failures and each rerun. Separate product failure from collection, setup, timeout or assertion errors. If a corrected version is available, run the same test unchanged on both versions. Functional sequence tests do not require a numeric performance SLO; permission for local synchronization does not authorize disrupting shared services.
5. **Close coverage, then report.** Revisit the material risks: which have observed evidence, which remain untested, and which lack an agreed oracle? A release blocker does not settle other important risks. Report findings with reproduction, expected/actual behavior and evidence, followed by consequential gaps. Keep shared metadata once and avoid repeating logs in prose. Never label unexecuted or uncertain work passed.

Use the user's language and project conventions. Testing alone does not authorize product fixes, deployment, publication or messages. Use owned synthetic/approved data and clean up only owned resources.

## Optional execution support

Use a native runner directly for short output. When repeated long logs obscure diagnosis, [run_check.py](scripts/run_check.py) preserves a separate complete log per attempt and prints the real exit code, elapsed time and a bounded tail:

```text
python3 <skill-dir>/scripts/run_check.py --out-dir <artifacts> --timeout 120 -- <native-test-command> <args>
```

It does not interpret exit zero as QA success. Inspect collection counts and relevant failure details in the log. It requires Python 3.9+ only if used; no language or framework is required by the skill.

## Reference index

Read the matching section when needed; return to execution once the question is resolved.

- Unclear scope or priorities: [scope and risk](references/scope-and-risk.md).
- A technique or coverage model needs precision: [test design](references/test-design.md).
- Setup, evidence or rerun handling is uncertain: [execution](references/execution-and-evidence.md); test placement or flaky automation: [automation](references/automation.md).
- Identity, protocol, cache, jobs or transactions: [services](references/services-and-distributed.md); stored data and migrations: [data](references/data-and-migrations.md).
- Browser, mobile, desktop, CLI or accessibility: [interfaces](references/interfaces-and-clients.md).
- Load, recovery, security-related QA or compatibility targets: [quality attributes](references/quality-attributes.md).
- Probabilistic/AI behavior: [AI testing](references/ai-testing.md); specialist constraints: [domain adaptation](references/domain-adaptation.md).
- Conflicting release evidence or reporting semantics: [results](references/results-and-decisions.md).
- ISTQB terminology and authoritative anchors: [sources](references/sources.md). This is independent guidance, not ISTQB accreditation or a guarantee of exhaustive QA.

Optional artifacts: [plan](assets/test-plan.md), [cases](assets/test-cases.md), [defect](assets/defect-report.md), [report](assets/test-report.md). Use them only when the deliverable needs that structure.
