#!/usr/bin/env python3
"""Check this repository's packaging and local links using Python 3.9+."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    sys.exit("Package validation requires development dependencies: "
             "python -m pip install -r requirements-dev.txt")


ROOT = Path(__file__).resolve().parents[1]
NAME = "lazyest-qa"
PLUGIN = ROOT / "plugins" / NAME
SKILL = PLUGIN / "skills" / NAME
errors = []


def check(condition, message):
    if not condition:
        errors.append(message)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def read_yaml_mapping(text, label):
    try:
        value = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        errors.append(f"Invalid YAML in {label}: {exc}")
        return {}
    if not isinstance(value, dict):
        errors.append(f"{label} must contain a YAML mapping")
        return {}
    return value


def required_string(mapping, field, label):
    value = mapping.get(field)
    check(isinstance(value, str) and bool(value.strip()),
          f"{label}.{field} must be a nonempty string")
    return value if isinstance(value, str) else ""


def validate():
    errors.clear()
    codex = read_json(PLUGIN / ".codex-plugin/plugin.json")
    claude = read_json(PLUGIN / ".claude-plugin/plugin.json")
    for manifest in (codex, claude):
        check(manifest["name"] == NAME, "Plugin name must match its directory")
        check(re.fullmatch(r"\d+\.\d+\.\d+", manifest["version"]),
              "Use a stable major.minor.patch release version")
        check(manifest["license"] == "MIT", "Manifest license must match LICENSE")
    for key in claude:
        check(claude[key] == codex.get(key), f"Plugin manifests disagree on {key}")
    check(codex["skills"] == "./skills/", "Codex must discover the shared skills directory")
    check("skills" not in claude, "Claude uses its default skills directory")

    for catalog_path, is_codex in ((".agents/plugins/marketplace.json", True),
                                   (".claude-plugin/marketplace.json", False)):
        catalog = read_json(ROOT / catalog_path)
        check(catalog["name"] == NAME, f"Unexpected marketplace name: {catalog_path}")
        check(len(catalog["plugins"]) == 1, "Expected one plugin per catalog")
        entry = catalog["plugins"][0]
        check(entry["name"] == NAME, "Catalog and plugin names must agree")
        source = entry["source"]
        if is_codex:
            check(source["source"] == "local", "Codex catalog must use a repository-relative source")
            source = source["path"]
        check(source == f"./plugins/{NAME}", "Catalog source must resolve to the shared plugin")
        check((ROOT / source).resolve() == PLUGIN, "Catalog source resolved incorrectly")

    entrypoint = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\n(.*?)\n---(?:\n|\Z)", entrypoint, re.S)
    check(frontmatter is not None, "SKILL.md requires YAML frontmatter")
    if frontmatter:
        metadata = read_yaml_mapping(frontmatter[1], "SKILL.md frontmatter")
        name = required_string(metadata, "name", "SKILL.md")
        check(name == NAME, "Skill name must match its directory")
        required_string(metadata, "description", "SKILL.md")

    ui = read_yaml_mapping((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"),
                           "agents/openai.yaml")
    interface = ui.get("interface")
    check(isinstance(interface, dict), "agents/openai.yaml.interface must be a mapping")
    if isinstance(interface, dict):
        for field in ("display_name", "short_description", "default_prompt"):
            required_string(interface, field, "agents/openai.yaml.interface")
        description = interface.get("short_description")
        if isinstance(description, str):
            check(25 <= len(description) <= 64, "UI short_description must be 25-64 characters")
        prompt = interface.get("default_prompt")
        if isinstance(prompt, str):
            check(f"${NAME}" in prompt, "UI default_prompt must mention the skill invocation")
    if "policy" in ui:
        policy = ui["policy"]
        check(isinstance(policy, dict), "agents/openai.yaml.policy must be a mapping")
        if isinstance(policy, dict) and "allow_implicit_invocation" in policy:
            check(isinstance(policy["allow_implicit_invocation"], bool),
                  "UI policy.allow_implicit_invocation must be a boolean")

    documents = [ROOT / "README.md", ROOT / "README.ko.md"]
    documents += list((ROOT / "docs").rglob("*.md")) + list(SKILL.rglob("*.md"))
    for document in documents:
        for target in re.findall(r"\[[^\]]*\]\(([^\s)]+)\)", document.read_text(encoding="utf-8")):
            parsed = urlsplit(target.strip("<>"))
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            resolved = (document.parent / unquote(parsed.path)).resolve()
            check(resolved.is_relative_to(ROOT), f"Link escapes repository: {document.relative_to(ROOT)}")
            check(resolved.exists(), f"Broken link: {document.relative_to(ROOT)} -> {target}")
    for path in PLUGIN.rglob("*"):
        check(not path.is_symlink(), f"Plugin must be self-contained: {path.relative_to(ROOT)}")
    check((ROOT / "LICENSE").is_file(), "Missing LICENSE")


if __name__ == "__main__":
    try:
        validate()
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        errors.append(f"Invalid or missing package data: {exc}")
    if errors:
        print("Package validation failed:\n" + "\n".join(f"- {error}" for error in errors))
        sys.exit(1)
    print("Package validation passed: manifests, catalogs, skill/UI YAML, and local links.")
