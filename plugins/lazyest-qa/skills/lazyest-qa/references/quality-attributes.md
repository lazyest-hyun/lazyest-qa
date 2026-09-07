# Quality attributes and specialist checks

Use for measurable non-functional questions. Select attributes from risks and requirements, not from a universal checklist. The [source map](sources.md) identifies specialist anchors; these procedures are practical adaptations. Domain compliance may need additional standards and qualified review.

## Define the measurement before running

For each selected attribute record the user consequence, target metric/criterion, workload or interaction, environment, duration/sample and decision rule. Use established requirements. Without them, propose explicit provisional targets or report observations; do not invent “industry standard” thresholds or choose a cutoff after seeing results.

## Performance and capacity

| Purpose | Shape | Evidence |
| --- | --- | --- |
| Expected load | Representative operation mix, concurrency/arrival rate and data size | Throughput, latency distribution, errors, saturation under that profile |
| Stress/capacity | Controlled increase to an agreed limit | Saturation point, degradation, rejection and recovery |
| Spike | Abrupt permitted change in demand | Queue/backpressure behavior, burst latency and recovery |
| Endurance/soak | Sustained workload for a justified interval | Resource growth, leaks, accumulated lag and stability |
| Volume | Representative large dataset/payload | Query/processing behavior and resource limits |

Define open arrival-rate versus closed-user workload, think time, warmup, measurement interval, dataset and dependency behavior. Bound load, duration and spend; preflight shared targets before generation.

Report p50/p95/p99 where sample size permits, throughput, failures/timeouts and resource/queue metrics, with units and sample counts. Do not rely on average latency or exclude timeouts without disclosure. Check that the generator is not saturated and that a slowdown did not silently reduce offered load (coordinated-omission risk).

Compare baseline/candidate under comparable conditions; state noise and environment differences. A microbenchmark, a few curl timings, or a local mock proves neither production capacity nor a service-level objective. Preserve test profile and raw summaries for reproduction. If realistic execution is unavailable, produce the workload/measurement plan and clearly label the runtime gap.

## Reliability, recovery and operability

Start from the failure model: process crash, dependency outage, network interruption, disk full, resource exhaustion, stale cache or unavailable zone. Inject only faults covered by scope and authority, preferably in an isolated environment.

Verify correct degraded behavior, bounded retry/backoff, cancellation, timeouts, recovery ordering and state integrity after return. Check the business effect as well as health signals. “Ready” at one instant does not establish backlog recovery or successful delivery.

For recovery requirements, measure recovery time and data loss against the project's RTO/RPO. Include restoring a usable service and data, not just starting a process. Test backup restoration independently. Observe alerts/diagnostics through approved test channels where authorized; do not silently send real pages or notifications.

For deployment/operations assessment, inspect candidate/configuration provenance, supported mixed-version behavior, migration dependencies, rollback/forward-recovery procedure and observability of critical outcomes. Reviewing these does not authorize deployment or chaos experiments.

## Security and privacy within QA

Select checks relevant to the feature: access matrix, input/output handling, session expiration, sensitive fields in responses/logs, uploaded-file handling, tenant isolation, and permitted data lifecycle. Use test-owned data and scoped actions. Security scanner output is a finding candidate requiring validation, not a proof of exploitation or absence of vulnerabilities.

For an explicitly requested security audit, penetration test or deep assessment, use available specialist workflows and current official guidance such as versioned OWASP WSTG/ASVS. If those tools are unavailable, state the scope you can assess and the specialist execution gap; do not install a dependency or claim completion automatically.

Distinguish an engineering privacy expectation from a legal compliance claim. Identify applicable requirements supplied by the organization; use authoritative current sources when normative interpretation matters. Do not certify compliance through a generic QA checklist.

## Compatibility, portability and maintainability

Select supported OS/browser/runtime/database/protocol versions, hardware constraints and coexistence directions. Test the relevant real combinations or identify simulation limits. “Compatible” needs a named matrix.

Exercise installation, upgrade, downgrade if supported, configuration migration, failed install cleanup and uninstall/data retention semantics. A successful build is not installation evidence.

For maintainability/testability reviews, inspect coupling affecting change isolation, diagnostics, reproducible environments, controllable clock/randomness and observable failures. Tie findings to demonstrated change/test cost or fault isolation. Do not treat arbitrary style preferences as release-blocking defects.

Accessibility/usability procedures are in [interfaces](interfaces-and-clients.md); probabilistic model quality is in [AI testing](ai-testing.md); hazardous or regulated behavior is in [domain adaptation](domain-adaptation.md).
