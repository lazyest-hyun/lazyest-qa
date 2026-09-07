# Scope, risk and test strategy

Use for scope selection, planning, acceptance criteria, or QA process review. See [sources](sources.md) for the foundation and management anchors; the operating choices below are adaptable heuristics.

## Discover a sufficient basis

Inspect supplied changes/specifications, project instructions, tests and runner configuration, contracts/schemas, architecture and relevant defect history. For a running product, inspect available UI/API and environment identity. Stop gathering background when it no longer changes the next testing decision.

| Context | Resolve without turning every field into a question |
| --- | --- |
| Object and baseline | Feature, paths/services, candidate commit/build, comparison version, flags |
| Intended outcome | User task, business rule, failure consequence, acceptance criteria |
| Oracle | Approved specification, contract, domain rule, reference data or independent model |
| Scope | Workflows, upstream/downstream dependencies and explicit exclusions |
| Execution | Tools, environments, access by reference, data and allowed effects |
| Constraints | Supported clients, deadlines, cost/load limits, specialist needs |
| Decision | What the user needs to decide and who owns acceptance |

Separate established requirements, working assumptions, and unresolved questions. If sources disagree, expose the conflict; old tests and current code do not automatically win. For missing requirements, derive useful examples and characterization observations, but label them provisional. A hypothesis is not an accepted release criterion.

## Review before execution

Inspect ambiguous terms, missing units, inclusive/exclusive bounds, absent/error inputs, interacting rules, states, timing, authorization and irreversible effects. “Fast,” “secure,” “supports mobile,” and “works correctly” require observable criteria.

Propose Given/When/Then examples when useful, including success and meaningful rejection/recovery. A status code rarely defines the entire user outcome. UAT establishes fitness for the actual user task; automated scenarios do not constitute stakeholder sign-off.

## Prioritize plausible harm

Write risks as **under condition X, failure Y could cause consequence Z**. Record likelihood and impact with reasons. Follow the team's model; absent one, use qualitative high/medium/low and identify uncertainty. Numeric likelihood × impact is optional prioritization, not a measured probability or an ISTQB-mandated scale. Low frequency does not make catastrophic harm unimportant.

| Context | Starting depth |
| --- | --- |
| Small isolated reversible change | Change/caller inspection, targeted behavior, adjacent regression |
| New feature or interacting rules | Rule/role/state cases, real boundary integration, key journey, exploration |
| Money, authorization, loss, concurrency, migration, shared dependency | Explicit invariants, denial/failure paths, interleavings/recovery, stronger traceability |
| Safety or regulated acceptance | Applicable domain requirements, qualified review, required independence and validated environments |

Trace beyond edited lines: callers, consumers, schemas, persistence, configuration, caches, async processing and older clients. Do not broaden a typo change into every specialist test.

## Evidence mix

| Level/activity | Question |
| --- | --- |
| Static review | Are requirements consistent and testable; is a defect visible without execution? |
| Component | Does an isolated rule/algorithm satisfy its behavioral contract? |
| Component integration | Do internal modules agree on protocol, data and failure behavior? |
| System | Does the complete product perform its task in its environment? |
| System integration | Does it work with external systems and their failure/version behavior? |
| Acceptance | Does it meet user/business, operational, contractual or applicable regulatory expectations? |

Use the smallest level capable of detecting each risk, then higher levels where wiring and real boundaries matter. Smoke is a viability selection; regression protects existing behavior; confirmation targets a repaired defect.

For broad assessments, mark relevant quality areas selected, deferred, unavailable, or not applicable with reasons. Consider correctness, interoperability, usability/accessibility, performance, reliability/recovery, security/privacy, maintainability/testability, installation/upgrade/portability, and domain safety. This menu is not a normative quality-model reproduction.

## Entry, exit and control

- Entry: identifiable candidate, usable environment, data/access, testable expectations and dependencies. A missing dependency may block only some tests.
- Exit: named risks and criteria have sufficient evidence; material defects/unmet criteria have dispositions. Propose criteria before results if none exist; keep them provisional until adopted.
- Suspend affected execution for a wrong target, contaminated results, effects outside authority, or reached time/load/cost limits. Continue unaffected work; resume once the blocker is resolved.
- Estimate by test families and setup/analysis using existing suite timing where available; state a range and uncertainty. Execute high-value cases early, subject to dependencies.
- Reprioritize when a failure exposes wider impact. Preserve deferred risks when time runs out.

## QA process improvement

Inspect escaped defects, late requirement changes, slow feedback, flaky suites, missing ownership, environment drift and inaccessible data. Identify a contributing process gap and propose a small change with an owner role and observable outcome. For example, use a consumer-contract check to prevent a demonstrated integration escape. Test count, defect count and coverage alone are not team productivity measures.

Adapt to cadence: iterative teams can carry risk/case links in work items; sequential projects may require baseline reviews; DevOps adds deployment/configuration and operational feedback. Preserve required artifacts without inventing bureaucracy.
