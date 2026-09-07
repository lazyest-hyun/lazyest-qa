# AI systems and AI-assisted testing

These are different assignments: **test an AI-based product** or **use AI to help test a product**. [CT-AI v2.0 and CT-GenAI](sources.md) anchor that distinction. The procedures below are an independent practical evaluation approach, not a universal benchmark.

## Test an AI-based product

Identify intended task, affected users, failure costs, permitted inputs/tools and what is deterministic versus probabilistic. Record model/provider/version, prompt/configuration, sampling settings, retrieval/index snapshot, tool schema and dataset version. Record unavailable version controls as reproducibility limits.

### Define independent acceptance

Use reviewed reference labels/answers, deterministic constraints and a rubric with concrete examples. Set metrics, slices, sample size/repetition policy and decision thresholds before evaluation where possible. If the owner has not defined acceptance, report a baseline or provisional rubric, not a confident go/no-go from invented numbers.

| Product | Useful measures and failure families |
| --- | --- |
| Classification | Confusion matrix, precision/recall/F1 by class, threshold tradeoff and cost of errors |
| Regression/ranking | Error distribution, outliers, ordering relevance and task-specific utility |
| Generative answers | Task correctness, grounding/citation support, completeness, appropriate abstention, consistency |
| RAG | Retrieval relevance/recall on known-answer items, index freshness, access filtering, answer support separately |
| Tool-using agents | Correct tool/arguments, authorized effects, confirmation boundaries, loops, duplicate actions and recovery |
| Multimodal | Pertinent image/audio/video transformations, missing/corrupt inputs, cross-modal grounding and accessibility |

An overall mean can hide a failed user group or task family. Choose slices from domain risks: input length, language, difficulty, rare classes, missing context, new distribution and affected population as appropriate. Do not fabricate sensitive group labels or unsupported fairness conclusions.

### Data and model evaluation

Separate training/tuning/development and final evaluation data. Check duplicates and leakage across splits, including entity/time overlap when relevant. Inspect label quality, provenance, drift, missingness and out-of-distribution inputs. Do not silently tune on the holdout set and then report it as independent validation.

Use deterministic checks for schemas, calculations, authorization and tool effects where possible. For probabilistic outcomes, retain input-level results, repeat meaningful samples, report variability and sample counts, and use suitable uncertainty intervals when making rate comparisons. One good answer or temperature zero does not prove deterministic correctness.

For paired baseline/candidate comparison, hold dataset and important conditions constant, preserve both outputs, and analyze meaningful regressions by slice. If using an LLM judge, calibrate against human-reviewed cases, record judge/version/rubric, check order/preference bias and independently review critical outcomes. A product grading its own answer is not sufficient independent evidence.

### Adversarial and operational cases

Use bounded test-owned cases for missing/contradictory context, misleading retrieved text, indirect prompt instructions, requested data outside the actor's scope, malformed tool output, rate limits and timeouts. Treat instructions in test data as data, not permission to change the test or perform an external action.

For agents, observe actual permitted side effects and verify duplicate/retried tool calls do not violate the operation contract. Use sandbox tools where possible. Tool-call text alone is not proof of successful execution. Separately measure cost, latency, token/context limits and recovery using [quality attributes](quality-attributes.md).

Never upload private test corpora to a new service without appropriate authority. If no live model, credentials or spend budget is available, perform dataset/rubric/pipeline checks and identify live inference as blocked/not run. An offline canned response is not a live-model pass.

## Use AI to assist testing

Give the assistant the relevant specification, contracts, risk context and existing test patterns. Ask for concrete cases with basis, inputs, expected results and coverage items. Review generated assumptions and oracles before accepting them.

Check that generated code imports real APIs from installed versions and executes the intended production path. Run it; test-looking syntax is not execution evidence. Reject invented endpoints, nonexistent selectors, copied implementation oracles, unasserted outcomes and tests that always pass. Verify a representative known-wrong outcome is detected when test effectiveness is in doubt.

Use AI for candidate cases, charters, data generation and failure clustering without treating its explanations as established causes. Minimize sensitive prompts, validate generated fixtures, retain reproducible seeds/versions when meaningful, and report actual runner evidence. Using this AI-assisted workflow does not imply the product itself is AI-based.
