# Domain adaptation and specialist boundaries

Use when the product has obligations or failure modes not adequately addressed by ordinary application tests. Apply the shared workflow and relevant routes first; add domain evidence because of concrete risk, not merely a category label.

| Domain | Establish before selecting cases | Additional evidence |
| --- | --- | --- |
| Financial calculations/payments | Units, precision, rounding, ledger and external-operation contract | Conservation, no unacceptable duplicate effects, reconciliation, cancellation/refund and recovery across partial failures |
| Embedded/IoT | Hardware/firmware versions, sensors/actuators, update and connectivity contracts | Reset/power-loss recovery, bad/stale sensor input, timing, communication faults and hardware-in-the-loop where needed |
| Real-time/safety-related | Hazards, safe state, deadlines, required integrity/assurance level | Worst-case timing under relevant conditions, fault response, required structural coverage, traceability and qualified independent review |
| Medical/regulated workflows | Intended use, applicable organization/jurisdiction requirements, required validation records | Approved scenarios, records/auditability, data integrity, validated environment and authorized acceptance |
| Games/interactive simulation | Gameplay invariants, device/input matrix, multiplayer consistency and frame budget | Save/load, state desynchronization, reconnect, deterministic/replay properties where promised, frame-time distribution |
| Search/recommendation | Relevance criteria, user/context slices, freshness and access rules | Reviewed relevance set, ranking regressions, cold/rare inputs, isolation and latency |
| Infrastructure/configuration | Desired state, allowed environments, dependencies and recovery plan | Configuration validation, isolated plan/dry-run limits, compatibility and runtime evidence where authorized |
| Legacy/poorly specified system | Observed behavior, business experts or trusted records, change objective | Characterization with explicit oracle uncertainty, change-focused regression, domain clarification |

## Build an extension without inventing obligations

1. Identify the actual domain requirement or harm and source it from supplied authoritative documents or current official sources.
2. State the invariant, hazard or acceptance condition in observable terms.
3. Choose a level, technique, dataset and representative environment capable of establishing it.
4. Add required independence, instrument calibration, traceability or specialist review only when grounded in the applicable regime or risk.
5. Record evidence and remaining gaps. Simulation, emulation and desk review have narrower claims than hardware or operational validation.

Do not invent standard clauses, certification requirements or legal applicability. Use the project's specified editions and qualified interpretation where required. A generic skill cannot grant a regulatory approval or replace a responsible acceptance authority.

For hardware or hazardous processes, do not energize actuators, induce unsafe physical states or change live control systems merely because a test was requested. Prepare the bounded simulation/bench procedure within actual authorization and leave unavailable physical evidence explicit.

## When the product is unfamiliar

Decompose it into inputs, state, decisions, outputs, interfaces, users, time and failure recovery. State unknown domain semantics. Apply techniques to what is established, ask targeted questions for materially missing oracles, and proceed with independent checks. Avoid claiming universal completion because every reference file was visited.
