# Interfaces, clients and human interaction

Use for user-facing systems. Select supported environments from product requirements, observed usage or an explicitly provisional matrix. Testing one desktop viewport does not establish all browsers or mobile hardware. [Sources](sources.md) provides mobile, usability and WCAG anchors; the scenarios below are practical applications.

## User journey before screen inventory

Identify role/persona, goal, entry point, starting data/state, critical actions and completion evidence. Cover a complete important journey, then selected failure and recovery paths. Inspect whether success is merely displayed or actually persisted. Do not create external business effects without applicable authority.

| Surface | High-value probes |
| --- | --- |
| Forms | Keyboard, paste/autofill/IME, invalid/missing inputs, stale data, submit twice, correction without losing valid input |
| Async pages | Initial/loading/empty/error/success, slow response, stale response after navigation, retry, optimistic update rollback |
| Navigation/session | Deep link, back/forward/reload, multiple tabs, expired session, switch actor/tenant, unsaved work |
| Collections | Search/filter/sort, pagination, no results, long content, deletion of the currently viewed item |
| Files/media | Upload/download/cancel, unsupported or corrupted data, progress, playback interruption, permission errors |
| Responsive appearance | Supported viewport breakpoints, zoom/text scaling, long translations, overflow, orientation |

Observe console/network only when available and relevant. A warning can be harmless; connect it to behavior before treating it as a defect. Distinguish visible functional failures, visual differences, accessibility failures and usability hypotheses.

## Accessibility

Use the project's target standard/version/level. If absent, a WCAG 2.2 AA-oriented check can be proposed as an engineering baseline, not an assumed legal requirement. Identify exact success criteria and exceptions from the official source before making a normative claim.

Combine automated checks with actual interaction where tools permit: keyboard reach/order, focus visibility and return, name/role/state, form errors, status announcements, zoom/reflow, contrast, alternatives for images/media, and motion/gesture alternatives. Record pages, states and assistive/browser combinations tested. Unavailable screen-reader or device checks remain explicit gaps.

Automated scanning cannot establish complete conformance. A visual screenshot cannot prove the accessible name, announced error or focus behavior. Conformance requires the applicable full-page and complete-process scope; do not label a sampled audit “fully WCAG compliant.”

## Usability and acceptance

Review clear feedback, understandable language, discoverability, error recovery and consistency against the user's goal. Label an expert heuristic review as such. For actual usability studies, specify representative participants, neutral tasks, success/time/error measures and consent/privacy arrangements. Do not invent participants or conclude that users find an interface easy merely because the agent completed it.

Prepare acceptance scenarios and evidence for the authorized stakeholder. Keep business acceptance separate from the agent's functional observations.

## Mobile and desktop lifecycle

| Dimension | Select cases based on the product |
| --- | --- |
| Installation/upgrade | Clean install, supported upgrade with existing data, failed/interrupted update, rollback/uninstall semantics |
| Process lifecycle | Background/foreground, suspend/resume, OS termination and relaunch, restored/unsaved state |
| Device integration | Permission grant/deny/revoke, camera/files/location, notifications/deep links, sensor unavailable |
| Connectivity | Offline start, reconnect, network handoff, conflict after offline edits, metered/slow network |
| Resources | Low storage/memory, battery constraints, thermal/performance limits where relevant |
| Display/input | Orientation, scale, keyboard/touch/pointer, shortcuts and native accessibility |

Use simulators/emulators for suitable checks but identify missing real-device evidence for hardware, background behavior, notifications, energy and OS integration. Browser mobile emulation is not equivalent to a native mobile app or a physical device.

For desktop products, include multi-window state, file associations, file locks, path/permission handling and OS-specific integration only where relevant. Do not run installers or OS changes merely to fill a matrix without applicable scope.

## CLI and libraries

For CLI tools, assert exit status, stdout/stderr contracts, stdin/pipes, empty input, filenames with spaces/Unicode, cancellation/signals and partial-output cleanup. Test both interactive and non-interactive behavior when supported. Help/version output is not a substitute for a real operation.

For libraries/SDKs, select public API contracts, error types, serialization, resource ownership, cancellation, thread/async guarantees and supported runtime versions. Test a minimal real consumer where packaging/import/type declarations are a risk.

## Localization and compatibility

Separate language, region and time zone. Test only promised combinations plus risk-driven boundaries: Unicode normalization, IME, bidirectional layout, long/plural text, date/number parsing, currency precision and daylight-saving transitions. Verify sorting/search semantics from the contract. Record the tested OS/browser/runtime versions and do not infer unsupported environments from a single passing run.
