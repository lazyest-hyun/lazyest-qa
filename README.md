# Lazyest-qa

Practical, ISTQB-informed software QA for **Codex and Claude Code**. Turn a quality question into suitable tests, actual execution evidence, and a clear account of remaining risks.

[한국어 안내](README.ko.md)

## Install in Claude Code

Run inside Claude Code:

```text
/plugin marketplace add lazyest-hyun/lazyest-qa
/plugin install lazyest-qa@lazyest-qa
```

Then invoke the plugin skill:

```text
/lazyest-qa:lazyest-qa Test this change and its affected flows using the existing project tools. Report defects and untested risks.
```

If Claude requests activation, run `/reload-plugins` or start a new session. The repeated name is the plugin namespace followed by the skill name.

## Install in Codex

Run in your terminal with a Codex CLI that supports plugins:

```sh
codex plugin marketplace add lazyest-hyun/lazyest-qa
codex plugin add lazyest-qa@lazyest-qa
```

Start a new task and select **Lazyest-qa** from the skills picker, or ask:

```text
Use the Lazyest-qa skill to test this change and its affected flows with the existing project tools. Report defects and untested risks.
```

Codex registers the plugin skill as `lazyest-qa:lazyest-qa`. The shorter `lazyest-qa` name belongs to a standalone installation.

### Codex: standalone skill alternative

If your client does not support plugin commands, ask Codex:

```text
Use $skill-installer to install the skill from
https://github.com/lazyest-hyun/lazyest-qa/tree/main/plugins/lazyest-qa/skills/lazyest-qa
```

Use `$lazyest-qa` after standalone installation. Choose either standalone or plugin installation to avoid duplicate entries. If a standalone copy already exists, use it or explicitly replace it when switching installation methods.

## What it does

- Review requirements for ambiguity, contradictions, missing oracles and acceptance criteria.
- Prioritize risks and derive concrete boundary, decision-table, state, combination, structural, property-based and exploratory tests.
- Execute authorized checks using the project's existing tools and investigate failures.
- Implement meaningful automated tests, diagnose flakiness, and verify fixes plus affected regression.
- Assess release evidence against established criteria without treating unrun tests as passes.

Routes cover interfaces, mobile/desktop/CLI, APIs and distributed systems, data and migrations, performance/recovery, accessibility/usability, security-related QA, AI evaluation and specialist domain needs.

## Example requests

```text
Use Lazyest-qa to derive test cases from this specification. Plan only; leave undecided business policies unresolved.
```

```text
Use Lazyest-qa to reproduce this defect, verify the supplied fix, and run relevant regression tests. Do not change product code.
```

```text
Use Lazyest-qa to assess this RAG release packet. Distinguish candidate-specific evidence from missing or unreliable evaluation results. Do not deploy.
```

The skill follows the user's language and the project's conventions. It has no required framework, operating system, account, paid service, MCP server or execution script. The host needs appropriate tools and access to execute the selected tests; unavailable checks remain explicit gaps.

## Design and limits

One entrypoint loads only the relevant parts of 12 references. Four optional templates support plans, cases, defects and reports. Small tasks can use ordinary tests and native runner output.

Results distinguish PASS, FAIL, BLOCKED, NOT RUN, INCONCLUSIVE, SKIPPED and NOT APPLICABLE. Oracle certainty is separate from execution status. A passing build, screenshot or mock has a limited evidential scope.

This is an independent practical skill, not an official ISTQB product or accreditation. It does not guarantee discovery of every defect or replace specialist validation where required. The repository contains original guidance and links, not copied syllabi or exam materials. See the [source map](plugins/lazyest-qa/skills/lazyest-qa/references/sources.md).

## Updates

For Claude Code:

```text
/plugin marketplace update lazyest-qa
/plugin update lazyest-qa@lazyest-qa
```

For a Codex CLI with plugin support:

```sh
codex plugin marketplace upgrade lazyest-qa
codex plugin add lazyest-qa@lazyest-qa
```

Release versions are kept in both plugin manifests; maintainers bump both when the plugin payload changes. Standalone copies must be updated separately.

## Repository layout

```text
.agents/plugins/marketplace.json       Codex catalog
.claude-plugin/marketplace.json        Claude Code catalog
plugins/lazyest-qa/
  .codex-plugin/plugin.json            Codex manifest
  .claude-plugin/plugin.json           Claude Code manifest
  skills/lazyest-qa/                   One shared skill source
```

## Validation and contributing

See [validation notes](docs/validation.md) for what was checked and its limits. Validate the package with Python 3.9 or later:

```sh
python3 scripts/validate.py
```

With Claude Code installed:

```sh
claude plugin validate .
claude plugin validate ./plugins/lazyest-qa
```

Change the shared skill once, keep the two manifests consistent, and include a concrete example demonstrating an improvement. Do not add project-specific paths, credentials or copied source manuals.

Original package content is available under the [MIT License](LICENSE). Referenced third-party materials retain their own terms and trademarks.
