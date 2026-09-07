# Design tests that discriminate

Start from expected behavior and plausible failure mechanisms. Name techniques only when their model and coverage items are present. This guidance combines standard concepts with original examples; [sources](sources.md) identifies the anchors.

## Select by problem shape

| Shape | Technique | Output / limit |
| --- | --- | --- |
| Inputs treated equivalently | Equivalence partitioning | Valid/invalid partitions and representatives; isolate invalid dimensions |
| Ordered limits, counts, dates, lengths | Boundary value analysis | Named partition edges and adjacent representable values |
| Interacting rules or permissions | Decision table | Feasible combinations and expected actions; explain impossible combinations |
| Lifecycle, retry, session, workflow | State transition testing | State/event/guard/effect model; valid/invalid transitions and relevant sequences |
| Many configurations | Combinatorial / pairwise / t-wise | Factors, values, constraints and verified interaction coverage |
| Related numeric dimensions | Domain testing | On/off boundary points across the multidimensional constraint |
| Entity lifecycle and relationships | CRUD and scenarios | Lifecycle operations with dependent resources, roles and persistence |
| Branch-heavy code | Statement/branch/condition analysis | Executed structural items plus meaningful outcome assertions |
| Invariants over many inputs | Property-based / randomized testing | Constrained generators, independent properties, seed and minimized failure |
| Difficult expected result | Metamorphic / differential testing | Justified relations or independent reference; investigate disagreement |
| Unknown behavior or usability | Exploration / error guessing | Charter, observations, examples, questions and coverage notes |

Combine techniques when they expose different failures; do not apply every technique to every object.

## Partitions and boundaries

Identify type, representation, ordered domain, unit and precision. Distinguish absent, null, empty, whitespace-only, malformed, wrong type, valid and out-of-range when the contract does. Keep unrelated inputs valid for an invalid-partition test to avoid masking by an earlier rejection.

Example: integer quantity valid **10 through 20** has partitions `<=9`, `10..20`, `>=21`. Ordinary limit probes are `9,10,11,19,20,21`.

For explicit **ISTQB CTFL BVA coverage** claims, specify the model:

- 2-value coverage of these partition boundaries uses `9,10,20,21`.
- 3-value coverage uses each boundary value and its neighbors. For boundary values `9,10,20,21`, the deduplicated set is `8,9,10,11,19,20,21,22`.
- The six ordinary probes are useful but do not cover all items of that full 3-value model. Do not label them 100% coverage.

For decimals/dates, use the contract's increment and representation, not a universal epsilon. Add interior representatives where useful. Independent limits do not establish cross-field interaction coverage.

## Decision tables

Separate conditions and actions. Model feasible rules, then collapse don't-care conditions only if outcomes are independent. Supply concrete data and an observable action for selected rules.

Example: export requires a valid session and a permitted role. Cover four Boolean combinations unless a state is impossible. A disabled button does not prove server enforcement. If ownership affects the result, include it. If rule precedence is unspecified, show the requirement gap and candidate outcomes rather than copying the code's choice.

## State and sequence coverage

Model `current state + event + guard -> next state + outputs/effects`. Distinguish state coverage, valid transitions, all transitions, and sequences. Visiting every state is weaker than exercising every transition.

For a job, model submit, claim, complete, cancel and expire as applicable. Select retries, duplicates, late events and restart sequences where effects matter. On invalid transitions assert no unauthorized state change or duplicate effect; isolate invalid events. Identify whose clock and which persistence boundary control time guards.

## Combinations and code structure

- Pairwise is not a few representative rows. Record factors/values/constraints and verify every feasible pair. Use higher strength or explicit cases for known multi-factor risks; pairwise does not cover all business rules.
- For `A and B`, branch coverage does not establish each condition's independent effect. Use condition coverage, MC/DC or multiple-condition coverage only where justified, with the chosen model and feasible independence pairs.
- Coverage shows execution, not oracle correctness. Bounded mutation testing may expose weak assertions; distinguish equivalent mutants and investigate meaningful survivors without imposing a universal score.
- Prefer public behavior over source-string checks or mock call counts that lack outcome assertions.

## Properties, metamorphic relations and fuzzing

Candidate properties include conservation, ordering, round-trip preservation, idempotency, monotonicity and isolation. Justify each from the contract: duplicate suppression is wrong for an operation intended to repeat effects.

Generate valid constrained inputs and targeted invalid families. Record seeds and shrink failures. Avoid duplicating the implementation's formula as the oracle.

A metamorphic relation predicts the result change under a justified transformation. Permuting independent records may preserve an aggregate, but not a sequence-dependent output. Agreement between two implementations is evidence, not proof; they can share defects. Fuzzing needs resource/time bounds and an interpretable crash detector or invariant.

## Exploration and acceptance

Charter: explore **surface**, with **data/persona/constraint**, to discover **risk**, within **timebox**. Record paths, inputs, failures and questions; turn important repeatable discoveries into regression cases when appropriate.

Acceptance cases express the user's objective with exceptions and recovery. Useful fields are ID, basis/risk, level/purpose, setup, exact data, action, expected output/state effects, cleanup and execution status. Use [case template](../assets/test-cases.md) when structured output helps.

Keep oracle certainty separate from execution status. A planned case with an unresolved rule is still NOT RUN; its expected behavior is unresolved. For mixed cases, separate established invariants from provisional or unknown outcomes so useful assertions can proceed without inventing the missing policy. Measurement/exploration without a decision threshold does not produce a pass/fail claim.
