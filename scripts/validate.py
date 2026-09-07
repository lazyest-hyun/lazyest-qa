#!/usr/bin/env python3
"""Check this repository's packaging and local links using Python 3.9+."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit


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


def validate():
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
    frontmatter = re.match(r"\A---\n(.*?)\n---\n", entrypoint, re.S)
    check(frontmatter is not None, "SKILL.md requires YAML frontmatter")
    if frontmatter:
        check(re.search(rf"(?m)^name: {NAME}$", frontmatter[1]), "Skill name must match its directory")
        check(re.search(r"(?m)^description: .+", frontmatter[1]), "Skill description is required")
    check(len(list(SKILL.glob("references/*.md"))) == 12, "Expected 12 reference routes")
    check(len(list(SKILL.glob("assets/*.md"))) == 4, "Expected four optional templates")
    check((SKILL / "agents/openai.yaml").is_file(), "Missing Codex skill UI metadata")

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
    print("Package validation passed: manifests, catalogs, shared skill, and local links.")
