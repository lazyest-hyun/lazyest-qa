---
name: lazyest-qa
description: Plan, design, execute, and assess software QA and testing using ISTQB-informed, risk-based methods. Use for test cases, exploratory QA, regression, test automation, defect verification, or release readiness across software products. Also handles requirements and test-process reviews. Not for certification exam tutoring or a standalone security audit.
---

# Lazyest-qa

Turn the requested quality question into appropriate tests, observable evidence, and an honest decision. Adapt to the product, lifecycle, risk, available tools, and requested depth. This is an independent practical skill, not an official ISTQB product, accreditation, or guarantee that all defects can be found.

## Start with the actual assignment

Read the supplied requirements, change, application, and relevant local instructions before selecting tests. Use the user's language for discussion and deliverables; retain the project's naming and test conventions. Paths below are relative to this skill directory. There is no required language, framework, browser, service, account, OS, or paid tool.

Choose the mode from intent; combine only where the assignment needs it:

| Request | Work to perform | Completion evidence |
| --- | --- | --- |
| Review requirements or QA process | Inspect testability, contradictions, prevention and feedback gaps | Source-linked findings, acceptance examples or process proposals |
| Plan / design / cases only | Derive risks, coverage items, concrete cases and execution order | Reviewable plan/cases; execution explicitly not performed |
| Test / QA / check this works | Discover the environment, design and perform authorized checks, investigate failures | Actual results and artifacts; blockers for unavailable checks |
| Add or improve automated tests | Identify missing behavioral coverage, implement in the existing stack and run | Executed tests with meaningful assertions and maintenance guidance |
| Verify a fix / regression | Reproduce the original trigger, test the change and affected neighbors | Confirmation result plus separately scoped regression results |
| Assess a release | Evaluate candidate-specific evidence against agreed exit criteria | Supported recommendation, open defects and residual risks |

If asked to execute, do not stop at a plan when execution is available. If asked only to inspect or plan, do not change the product, test suite, environment, or external records. Testing permission does not silently authorize product fixes, publication, deployment, or sending messages. Honor existing authorization without repeatedly asking.

## Working loop

1. **Establish context.** Identify object/version, user outcomes, test basis and oracle, scope, environment/data, and permitted actions. Inspect discoverable facts first. Ask only for missing facts that change expected behavior, scope, or execution safety; continue independent work. Use [scope and risk](references/scope-and-risk.md) for broad or ambiguous assignments.
2. **Select coverage.** Trace affected behavior and dependencies. Rank plausible failure modes, choose levels and quality characteristics, then read relevant routes below. For “test everything,” account for relevant surfaces and explicit exclusions; do not execute every catalog entry indiscriminately. A tiny change can need only a few checks.
3. **Design discriminating tests.** Turn each important risk or rule into a condition, data, action, and observable expected outcome. Apply [test design](references/test-design.md) when deriving cases; identify the technique's actual coverage items, not just its name. Do not derive the oracle solely from the implementation under test.
4. **Prepare and execute.** Read [execution and evidence](references/execution-and-evidence.md) before dynamic testing. Use existing runners and authorized tools. Verify the target, run a useful small check first, then cover selected risks. Capture reproducible failure evidence.
5. **Investigate and adapt.** Distinguish product defects, incorrect tests, environment failures, and unresolved requirements. Preserve first failures and reruns. New evidence may justify targeted expansion; repeated clean runs without a reason do not.
6. **Close the loop.** Use [results and decisions](references/results-and-decisions.md). Connect conclusions to tested versions, coverage and evidence; list material gaps. If fixes are authorized, verify the original failure and relevant regression after the fix. Otherwise provide a reproducible defect and next step.

## Read only needed routes

Select by failure mechanism, not a single technology keyword. Combine routes for cross-boundary flows.

| Trigger or object | Reference | Decision |
| --- | --- | --- |
| New feature, unknown scope, strategy, UAT, process improvement | [Scope and risk](references/scope-and-risk.md) | What matters and how much evidence is justified |
| Inputs, decisions, states, combinations, branches, exploration | [Test design](references/test-design.md) | Which technique exposes the likely defect |
| Run tests, prepare data/environment, investigate failures | [Execution and evidence](references/execution-and-evidence.md) | What can run and what the result proves |
| Unit/integration/E2E, CI, flaky tests, mocks | [Automation](references/automation.md) | Test placement and trustworthy assertions |
| APIs, auth, queues, concurrency, transactions | [Services and distributed systems](references/services-and-distributed.md) | Contracts and effects across identity, failure and time |
| Web, mobile, desktop, CLI, accessibility, usability, localization | [Interfaces and clients](references/interfaces-and-clients.md) | User journeys across interaction environments |
| Databases, migrations, ETL, analytics, exports | [Data and migrations](references/data-and-migrations.md) | Integrity, semantics, reconciliation and recovery |
| Load, recovery, compatibility, security/privacy | [Quality attributes](references/quality-attributes.md) | Measurable targets and adequate environments |
| ML, LLM, RAG, agents, AI-generated tests | [AI testing](references/ai-testing.md) | Probabilistic evaluation and validation of generated tests |
| Embedded, real-time, hardware, finance, regulated systems, games | [Domain adaptation](references/domain-adaptation.md) | Additional domain or specialist evidence |
| Defects, progress, reporting, release recommendation | [Results and decisions](references/results-and-decisions.md) | Supported conclusions and remaining gaps |
| Terminology, source versions, skill maintenance | [Source map](references/sources.md) | Official anchors versus independent extensions |

## Proportionality and coverage

- Distinguish **level** (component, component integration, system, system integration, acceptance), **quality characteristic** (e.g. correctness or performance), **technique** (e.g. boundaries), and **purpose** (e.g. smoke, confirmation, regression). One test can have all four.
- Use static reviews to expose ambiguity and design defects early. QA also concerns prevention and process improvement; passing dynamic tests alone is not a complete QA process.
- Target meaningful behavior and risk. Do not impose a universal test count, coverage percentage, pyramid ratio, performance threshold, client matrix, or release gate.
- A green build, mock, screenshot, successful HTTP response, scan, or high code coverage has a specific evidential limit. Report coverage and omissions.
- Never mark planned, skipped, blocked, or unobserved tests as passed. Unknown expected behavior is an oracle gap; do not invent policy to manufacture a result.
- Do not weaken assertions, refresh snapshots, disable tests, or add retries merely to make failures disappear. Validate intended behavior first.
- Prefer synthetic or approved sanitized data. Limit cleanup to owned test resources and keep unnecessary sensitive data out of shared evidence.

## Deliverables and invocation

Use existing project formats. Respond inline for small work. For substantial work, adapt only needed templates: [plan](assets/test-plan.md), [cases](assets/test-cases.md), [defect](assets/defect-report.md), [report](assets/test-report.md). These are aids, not mandatory paperwork. Store evidence in the project's artifact location, not the installed skill.

- “Use $lazyest-qa to test this change and its affected flows with the existing test tools.”
- “Use $lazyest-qa to derive boundary and decision-table cases from this specification. Plan only.”
- “Use $lazyest-qa to verify this fix and identify regression gaps.”
- “Use $lazyest-qa to assess release readiness from these reports; do not deploy.”
- “Use $lazyest-qa to evaluate this RAG assistant with the supplied dataset and budget.”
