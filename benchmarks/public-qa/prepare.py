#!/usr/bin/env python3
"""Prepare historical source snapshots from an existing local git clone. No network."""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tarfile


def git(repo, *arguments):
    return subprocess.check_output([
        "git", "--no-lazy-fetch", "--no-replace-objects",
        "-c", "protocol.allow=never", "-C", str(repo), *arguments,
    ])


def snapshot(repo, commit, destination):
    """Extract a pinned git archive without accepting escaping paths or special files."""
    destination.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(git(repo, "archive", commit)), mode="r:") as archive:
        for member in archive:
            target = destination / member.name
            target.resolve().relative_to(destination.resolve())
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            elif member.isfile():
                target.parent.mkdir(parents=True, exist_ok=True)
                with archive.extractfile(member) as source:
                    target.write_bytes(source.read())
                target.chmod(member.mode & 0o777)
            elif member.issym():
                (target.parent / member.linkname).resolve().relative_to(destination.resolve())
                target.parent.mkdir(parents=True, exist_ok=True)
                target.symlink_to(member.linkname)
            else:
                raise ValueError("Unsupported archive entry: " + member.name)


def hashes(directory):
    result = {}
    for path in sorted(directory.rglob("*")):
        if path.is_symlink():
            value = b"symlink:" + os.readlink(path).encode()
        elif path.is_file():
            value = path.read_bytes()
        else:
            continue
        result[str(path.relative_to(directory))] = hashlib.sha256(value).hexdigest()
    return result


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="Existing tornadoweb/tornado git clone")
    parser.add_argument("--out", required=True, type=Path, help="New output directory; must not exist")
    args = parser.parse_args()
    source = Path(__file__).resolve().parent
    manifest = json.loads((source / "manifest.json").read_text(encoding="utf-8"))
    repo, output = args.repo.resolve(), args.out.resolve()
    if output.exists():
        parser.error("--out already exists; choose a new directory. Nothing was removed.")
    # Validate every required object before creating output. Never fetch or checkout.
    for case in manifest["cases"]:
        for state in ("buggy", "fixed"):
            commit = case[state + "_commit"]
            resolved = git(repo, "rev-parse", commit + "^{commit}").decode().strip()
            if resolved != commit:
                raise ValueError("Commit did not resolve exactly: " + commit)
            git(repo, "cat-file", "-e", commit + ":LICENSE")
        git(repo, "cat-file", "-e", case["fixed_commit"] + ":" + case["gold_test_file"])
    output.mkdir(parents=True, exist_ok=False)
    evaluator = output / "evaluator-only"
    evaluator.mkdir()
    write_json(evaluator / "manifest.json", manifest)
    provenance = {"source_repo": str(repo), "upstream": manifest["upstream"], "cases": []}
    for case in manifest["cases"]:
        case_dir = output / "cases" / case["id"]
        blind = case_dir / "input"
        private = evaluator / case["id"]
        private.mkdir()
        snapshot(repo, case["buggy_commit"], blind)
        (case_dir / "TASK.md").write_bytes((source / case["task_template"]).read_bytes())
        (case_dir / "result").mkdir()
        shutil.copytree(blind, private / "buggy", symlinks=True)
        snapshot(repo, case["fixed_commit"], private / "fixed")
        gold_path = case["gold_test_file"]
        gold = git(repo, "show", case["fixed_commit"] + ":" + gold_path)
        target = private / "gold" / gold_path
        target.parent.mkdir(parents=True)
        target.write_bytes(gold)
        # Keep the upstream license alongside the separately stored gold file too.
        (private / "gold" / "LICENSE").write_bytes((private / "fixed" / "LICENSE").read_bytes())
        for state in ("buggy", "fixed"):
            (private / state / gold_path).write_bytes(gold)
        inventories = {
            "input": hashes(blind),
            "buggy": hashes(private / "buggy"),
            "fixed": hashes(private / "fixed"),
            "gold": hashes(private / "gold"),
        }
        write_json(private / "hashes.json", inventories)
        python_files = list(blind.rglob("*.py"))
        provenance["cases"].append({
            "id": case["id"], "buggy_commit": case["buggy_commit"],
            "fixed_commit": case["fixed_commit"],
            "gold_sha256": hashlib.sha256(gold).hexdigest(),
            "python_files": len(python_files),
            "python_lines": sum(len(path.read_bytes().splitlines()) for path in python_files),
            "input_sha256": hashlib.sha256(json.dumps(inventories["input"], sort_keys=True).encode()).hexdigest(),
        })
        print("Prepared " + case["id"])
    write_json(evaluator / "provenance.json", provenance)
    print("Share only cases/<id>/ with a participant. Keep evaluator-only/ inaccessible.")


if __name__ == "__main__":
    main()
