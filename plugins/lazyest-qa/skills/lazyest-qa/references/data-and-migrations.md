# Data, migrations and pipelines

Use where correctness depends on durable data or transformations. Combine with [services](services-and-distributed.md) for transaction/event boundaries. The examples are original engineering guidance; follow the actual database, pipeline and domain contracts.

## Establish semantics

Identify source of truth, schema versions, keys, units, precision, time zone, ownership and retention rules. Determine whether missing, null, zero and empty are distinct. Derive expected results from reviewed fixtures or an independent calculation; the same transformation code is not an independent oracle.

| Risk | Test and evidence |
| --- | --- |
| Integrity | Uniqueness, references, constraints, allowed nulls and rejected writes |
| Precision | Decimal rounding, overflow, aggregation order and supported units |
| Time | Boundary timestamps, zone conversion, daylight saving, event time vs processing time |
| Partial writes | Fault at intermediate write, transaction rollback/commit, durable final state |
| Isolation | Conflicting updates, optimistic version rejection, selected concurrent schedules |
| Scope | Tenant/owner isolation including joins, exports and caches |
| Deletion/retention | Intended delete/archive cascade, restored visibility, downstream artifacts and retention behavior |
| Reconciliation | Source/target keys, counts, missing/extra rows, aggregates and semantic value comparisons |

Row counts alone do not prove correct values or relationships. Compare keys and invariants and inspect representative/boundary records. Explain sampling and any excluded partitions.

## Migration and upgrade

Test against a disposable instance or an explicitly authorized environment, using the actual engine/version when behavior depends on it. Review destructive statements, locks, transaction boundaries and execution hooks before running.

1. Create a representative old-version fixture: non-empty tables, edge values, duplicates if historically possible, and relationships affected by the change.
2. Run the migration and validate schema plus semantic data integrity. Empty-database success is insufficient for an upgrade claim.
3. Verify supported application/schema combinations during rollout, including old clients if they may coexist. Separate expand, migrate/backfill and contract phases when the design uses them.
4. Test interruption, rerun/resume and concurrent writes according to the promised migration behavior. Do not assume a migration is idempotent unless its contract requires it.
5. Exercise rollback or forward recovery if supported. State unrecoverable data loss explicitly rather than treating a schema rollback as restoration.
6. Assess lock duration and data-volume risk in an appropriate environment. Small local fixtures prove semantics, not production migration time.

Backup creation is not recovery evidence. When recovery is in scope, restore to an isolated target, check integrity and application usability, and measure against the agreed recovery objectives.

## ETL, streaming and analytics

Trace extraction, transformation, join/deduplication, load and aggregation. Select empty batch, schema drift, malformed rows, late/out-of-order events, duplicate/replayed batches, partial failures and watermark boundaries.

Assert business semantics: deduplication key/window, join cardinality, null treatment, aggregation grain, lineage and freshness. Verify replay and recovery do not silently lose or multiply records under the promised processing semantics. A job's successful exit does not prove the output dataset is correct.

For reports and analytics, check denominator definitions, time windows, filters, pagination and distinct-versus-total counts. A metric total is not automatically a unique-user count. Compare an independently calculable fixture with the displayed and exported values.

## Import/export and files

Check encoding, delimiters/escaping, embedded newlines, Unicode, very long values, empty files, formula-like spreadsheet cells where relevant, and round-trip semantics. Match precision and null representation to the format contract. Verify partial/cancelled operations do not leave misleading success artifacts.

## Test-data lifecycle

Use synthetic fixtures that preserve the relationships needed to expose defects. If realistic sanitized data is necessary, confirm permitted use and destination. Minimize collected records and redact evidence. Unique run IDs and scoped cleanup prevent one run from modifying another's state; report any leftovers and their owner/location without exposing secrets.
