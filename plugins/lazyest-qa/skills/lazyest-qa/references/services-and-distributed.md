# Services, APIs and distributed behavior

Use for contracts, identities, persistence boundaries and asynchronous/concurrent effects. Combine with [data](data-and-migrations.md), [quality attributes](quality-attributes.md), and [test design](test-design.md) as needed. This is a practical engineering extension, not an ISTQB protocol specification.

## Build a boundary map

Identify caller -> handler -> policy -> storage -> event/dependency -> user-visible result. Record which boundaries are real, simulated or unavailable. Derive expectations from the versioned contract and business rules. A 200/202 response is not evidence of every downstream effect.

| Concern | Cases to select | Assert |
| --- | --- | --- |
| Request validation | Missing/null/empty, wrong type, overflow, encoding, duplicate parameters, unknown fields | Contract-specific response and absence of invalid writes |
| Response contract | Success/error schemas, content type, field presence/nullability, precision | Consumer-visible semantics, not just status |
| Identity and scope | Anonymous, expired/revoked identity, role, owner/non-owner, tenant A/B | Server-side allow/deny across read/write/list/export and nested resources |
| Pagination/filter/order | Empty and last page, ties, cursor invalidation, inserts between pages | Stable contract semantics; no unexplained missing/duplicate results |
| Version compatibility | Older/newer producer/consumer, optional/required fields, enums | Actual supported compatibility directions |
| Retry/idempotency | Same operation/key, changed payload, concurrent replay, key expiry | The contract's number of effects and consistent replay semantics |
| Dependency failure | Timeout before/after acceptance, malformed response, rate limit, unavailable dependency | Defined user state, retry/recovery and no silent loss |
| Caching | Cold/warm, update/invalidate, expiry, identity/tenant switch | Freshness bound and scope isolation |
| File/stream transfer | Truncation, disconnect, large/empty payload, resume | Integrity, bounded resource use and cleanup |

Avoid assuming every API must return the same status for a denial or malformed input. Establish the contract and leakage implications before classifying a mismatch.

## Authorization matrix

Cross operation, actor role, ownership/tenant and resource state. Include direct API access even if the UI hides an action. Check list/search/count/export and child-resource references when they can reveal protected data. Verify rejected operations did not mutate state. Distinguish authentication (who) from authorization (which action/resource).

Use test-owned actors and records. Ordinary role checks do not authorize a broad vulnerability scan; route an explicitly requested security audit to available specialist procedures.

## Concurrent mutations

State the invariant before generating load: e.g. no more than available stock is allocated; one accepted transfer produces one ledger effect; an acknowledged update is not silently overwritten. Select realistic interleavings:

1. Both requests read the same prior state.
2. One operation commits while another times out or retries.
3. A stale writer attempts a conflicting update.
4. The same idempotency key arrives concurrently or with a different payload.

Use a deterministic barrier where possible and verify durable final state after all workers finish. Check both response outcomes and conservation/uniqueness invariants. A client-side disabled button cannot establish server atomicity. Replica lag does not establish writer correctness; test the promised consistency model and stale-read behavior explicitly.

## Queues, jobs and events

Define delivery guarantees and ownership/lease rules from the system contract. Test duplicate, delayed and out-of-order deliveries, retry exhaustion, poison messages, worker restart, lease expiration and versioned payloads when relevant.

Use fault points at meaningful boundaries: before persistence, after persistence but before publish/ack, after an external effect but before local confirmation. Verify recovery produces neither unacceptable loss nor extra effects. Outbox/inbox or deduplication mechanisms need evidence of the intended invariant under replay; the name of a pattern is not proof.

Observe accepted, queued, running, completed/failed and externally delivered states separately. Correlate IDs and bound waiting by the agreed completion expectation. Distinguish a missing event from an observation channel that is delayed or unavailable.

## Contracts and real dependencies

Keep fake-service cases for deterministic adverse responses. Also select a test against the real dependency's authorized test environment when protocol or integration behavior is a material risk. If unavailable, report simulation coverage and the remaining integration gap. Capture provider acceptance and business completion separately, and keep secrets out of traces.

For load/backpressure, see [quality attributes](quality-attributes.md). A functional concurrency test proves selected interleavings, not production capacity. For schema changes and persisted state, see [data and migrations](data-and-migrations.md).
