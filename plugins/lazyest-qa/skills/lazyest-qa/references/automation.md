# Automation and test-suite quality

Use for writing, repairing or choosing automated tests. Apply [execution preflight](execution-and-evidence.md) before running. Automation engineering is anchored in [CTAL-TAE](sources.md); examples here are framework-neutral implementation guidance.

## Discover and fit the existing stack

Read manifests, scripts, test configuration, fixture helpers and CI workflows. Find a nearby representative test and the actual production call path. Use documented commands and installed versions. Do not add another framework, cloud runner or orchestration layer merely because it is familiar.

For a small local component, ordinary tests and captured native runner output usually suffice. Evidence collection does not require a custom JSON reporter, runtime audit hooks or a new runner. Add such machinery only for an actual reporting or instrumentation requirement that simpler tools cannot meet.

| Boundary to establish | Typical placement |
| --- | --- |
| Pure rule, parser, calculation | Component tests with representative, boundary and property inputs |
| Database behavior, uniqueness, isolation, query semantics | Integration with the actual database engine or a faithful test instance |
| Protocol and consumer compatibility | Contract/schema checks plus provider/consumer verification |
| Service orchestration and failure recovery | Integration using controlled dependency responses, with real-boundary checks where needed |
| A user's critical journey | A small number of system/E2E tests using the assembled product |
| Appearance or interaction semantics | Focused visual/UI tests plus human/assistive checks as applicable |

Choose placement by what the test must prove. No fixed pyramid ratio is required. A mocked database cannot establish transaction isolation; a mocked payment response cannot establish provider delivery.

## Write tests with a meaningful oracle

- Name behavior and condition. Arrange known state, perform the production-facing action, assert user-visible output and relevant durable effects.
- Derive expected values independently from the requirement or a reviewed reference fixture. Do not reproduce the same algorithm and call the equality check independent validation.
- Test success, rejection and important recovery conditions. Assert forbidden side effects stay absent as well as required effects appearing.
- For defects, add the smallest case exposing the original failure. Show it fails on the old behavior when practical and safe, then passes with the fix. If that comparison was not run, state it.
- Use parameterization for the same rule with different data. Keep unrelated outcomes in separate cases so failures explain themselves.
- Mock controlled external boundaries, not the core behavior being asserted. Record which results are simulation evidence. Where mocks can drift, add real contract/integration checks.

## Isolation, time and repeatability

Use per-test fixture ownership, deterministic seeds, injected/fake clocks for time rules, bounded waits for actual asynchronous completion, and explicit teardown. Avoid order dependence and global state leaks. Verify a critical new test can run independently when shared-state behavior is a concern.

Synchronize race tests at the vulnerable point: two requests should both reach the contested decision before either finalizes when that is the intended interleaving. A sleep-based schedule is not proof of contention. Preserve the chosen isolation level and concurrency model in the evidence.

For UI tests, select stable semantic targets from observed UI, wait for meaningful readiness, and assert behavior. Do not use broad forced clicks or fixed sleeps to hide genuine usability/timing failures. Visual baselines need stable fonts, viewport, animations and data; compare intended changes before approving new baselines.

## Validate the test itself

First run the focused test, then the affected suite and required project checks. Confirm tests were collected and assertions reached. Probe one representative wrong behavior or controlled negative fixture when oracle effectiveness is uncertain. Mutation/property tests are optional where they add confidence; do not test every trivial edit through an elaborate harness.

A passing assertion on a never-entered branch, a skipped test or a swallowed exception is not coverage. Check that failure paths actually produce the expected error and that cleanup does not suppress test failures.

## CI and maintenance

Select fast deterministic checks for change feedback, integration checks when dependencies are ready, and scheduled heavier suites only when the project requests them. Recommend a cadence without silently creating a scheduler or changing release gates.

Keep artifact retention and credentials scoped. Failures should identify candidate, command, case, environment and useful evidence. Distinguish product failure, infrastructure failure, flaky execution and no-tests-collected.

On flakiness, preserve first failure and retry history, minimize the cause, and repair isolation/synchronization or the product as appropriate. Quarantine is a temporary visible gap with owner and revisit criterion. Do not replace real assertions with snapshots or increase retries until a build becomes green.

Useful maintenance signals include defect detection value, feedback time, investigation cost, flake rate with denominator, and obsolete-case burden. Retire redundant tests only after checking which risks and callers they protect. New tooling is justified by a concrete capability gap and bounded evaluation, not by breadth of its feature list.
