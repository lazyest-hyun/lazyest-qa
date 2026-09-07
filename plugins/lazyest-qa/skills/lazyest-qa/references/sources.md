# Source map and maintenance

Research checked: **2026-09-06 to 2026-09-07**. This package contains independently authored operating instructions and examples. It does not reproduce ISTQB syllabi or examination materials and is not affiliated with or accredited by ISTQB. ISTQB is a registered trademark of the International Software Testing Qualifications Board.

## Official anchors

The four core PDF sources were inspected selectively for concepts and structure relevant to the skill, not reproduced as manuals. Specialist pages establish their published scope; they do not constitute a full study or implementation of every specialist syllabus. Version labels below identify consulted material, not a promise to remain the newest edition.

| Source inspected | Concepts used as anchors | Where applied |
| --- | --- | --- |
| [CTFL syllabus v4.0.1](https://istqb.org/wp-content/uploads/2024/11/ISTQB_CTFL_Syllabus_v4.0.1.pdf), especially test levels, static testing, sections 4.2–4.5 and chapter 5 | Test basis, systematic design, risk and reporting | Scope, test design, evidence and results |
| [CTAL Test Analyst v4.0](https://istqb.org/wp-content/uploads/sdm-uploads/ISTQB-CTAL-TA-Syllabus-v4.0-EN.pdf), work-product/oracle and design topics | Oracle/data quality and selection of analytical techniques | Test design, cases and data |
| [CTAL Technical Test Analyst v4.0](https://www.istqb.org/wp-content/uploads/2024/11/ISTQB-CTAL-TTA_Syllabus_v4.0.pdf), structural and technical-quality topics | Structural coverage and technical testing scope | Test design and quality attributes |
| [CTAL Test Automation Engineering v2.0](https://www.istqb.org/wp-content/uploads/2024/11/ISTQB_CTAL-TAE_Syllabus_v2.0.pdf), automation preparation and engineering structure | Context-sensitive automation design and evaluation | Automation |
| [CTAL Test Management v3.0](https://istqb.org/certifications/certified-tester-advanced-level-test-management-ctal-tm-v3-0/), official content overview | Risk, strategy, monitoring, defects and process improvement | Scope and results |
| [Performance Testing](https://istqb.org/certifications/certified-tester-performance-testing-ct-pt/), official content overview | Workload, measurements and lifecycle of performance assessment | Quality attributes |
| [Mobile Application Testing](https://istqb.org/certifications/certified-tester-mobile-application-testing-ct-mat/), official content overview | Device, connectivity and mobile-environment concerns | Interfaces and clients |
| [Usability Testing](https://istqb.org/certifications/certified-tester-usability-testing-ct-ut/), official content overview | Usability reviews, user studies and accessibility evaluation | Interfaces and clients |
| [Acceptance Testing](https://istqb.org/certifications/certified-tester-acceptance-testing/), official content overview | Business acceptance criteria and stakeholder collaboration | Scope and results |
| [Quality in DevOps](https://istqb.org/certifications/certified-tester-quality-in-devops-ct-qdo/), official content overview | QA across delivery and operational feedback | Scope, automation and quality attributes |
| [AI Testing v2.0](https://istqb.org/certifications/certified-tester-ai-testing-ct-ai/), official content overview | Testing data, models and generative AI systems | AI testing |
| [Testing with Generative AI](https://istqb.org/certifications/gen-ai/), official content overview | Using GenAI in testing and evaluating its output | AI-assisted testing |
| [W3C WCAG 2.2](https://www.w3.org/TR/WCAG22/), criteria and conformance scope | Explicit accessibility criteria and assessment limits | Interfaces and clients |
| [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/), project and version guidance | Source for deeper scoped web-security methodology | Quality attributes |
| [OpenAI: Build skills](https://learn.chatgpt.com/docs/build-skills), skill format and discovery | Portable entrypoint, relative references and progressive loading | Package structure and UI metadata |

## Interpretation boundaries

ISTQB testing principles motivate context-sensitive scope, early feedback, varied tests, attention to defect concentration and user needs, and honest limits on what testing establishes. The package operationalizes those ideas rather than supplying certification lessons.

Request modes, route selection, templates, status mapping, release wording and qualitative risk choices are this skill's conventions. Distributed-system invariants, detailed migration procedures, CI practices, property/mutation examples and AI evaluation operations are practical engineering extensions. Do not present these as verbatim ISTQB requirements or mandatory numeric standards.

WCAG and OWASP supplement the ISTQB anchors. A selected check is not a full compliance assessment or security audit. Domain standards, technology-specific behavior and required versions must come from the actual project and current authoritative sources.

## When to consult sources again

- For ordinary QA, use the project's current basis and relevant local reference; do not reread all external sources on every invocation.
- Verify the official source when a terminology detail, exact coverage model, normative criterion, version or compatibility claim affects the result.
- To update the skill, check the [official certification catalog](https://istqb.org/certifications/) and the linked course/download page. Record the inspected edition and changed scope. Do not silently label a retiring syllabus as the current default.
- If offline, use the recorded concepts with their date/version and disclose any unresolved current-standard question. Lack of internet does not block ordinary local testing against an established project contract.
- Preserve attribution, original examples and bounded reference loading. Do not bundle copied exams, syllabi, private project artifacts, credentials or user-specific paths.
