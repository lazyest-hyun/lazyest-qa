#!/usr/bin/env python3
"""Verify existing suites and upstream regressions; this does not run a model."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

# Importing our helper must not add an untracked bytecode file to the checkout.
sys.dont_write_bytecode = True
from prepare import hashes, write_json


def summary(text):
    runs = re.findall(r"^Ran (\d+) tests? in ", text, flags=re.MULTILINE)
    counts = {"tests": int(runs[-1]) if runs else None, "failures": 0, "errors": 0, "skipped": 0}
    ending = re.findall(r"^(?:OK|FAILED)(?: \(([^\n]+)\))?$", text, flags=re.MULTILINE)
    for key, value in re.findall(r"(failures|errors|skipped)=(\d+)", ending[-1] if ending else ""):
        counts[key] = int(value)
    counts["completed"] = bool(runs and ending)
    return counts


def integrity(root, case):
    private = root / "evaluator-only" / case["id"]
    expected = json.loads((private / "hashes.json").read_text(encoding="utf-8"))
    dirs = {"input": root / "cases" / case["id"] / "input"}
    dirs.update({state: private / state for state in ("buggy", "fixed", "gold")})
    return {name: hashes(directory) == expected[name] for name, directory in dirs.items()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Prepared benchmark directory")
    parser.add_argument("--out", required=True, type=Path, help="New verification report directory")
    parser.add_argument("--python", default=sys.executable, help="Python executable; validated with CPython 3.9.6")
    parser.add_argument("--timeout", type=float, default=45, help="Seconds allowed per native unittest command")
    args = parser.parse_args()
    root, output = args.root.resolve(), args.out.resolve()
    if output.exists():
        parser.error("--out already exists; choose a new directory. Nothing was removed.")
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    manifest = json.loads((root / "evaluator-only" / "manifest.json").read_text(encoding="utf-8"))
    for case in manifest["cases"]:
        protected = [root / "cases" / case["id"], root / "evaluator-only" / case["id"]]
        if any(output == directory or directory in output.parents for directory in protected):
            parser.error("--out must be outside participant and evaluator snapshot directories")
    before = {case["id"]: integrity(root, case) for case in manifest["cases"]}
    if not all(all(states.values()) for states in before.values()):
        parser.error("Snapshot hash mismatch; verification did not run.")
    output.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONNOUSERSITE="1")
    env.pop("PYTHONPATH", None)
    runtime_command = [args.python, "-c", "import json,platform,sys; print(json.dumps({'executable':sys.executable,'version':sys.version,'platform':platform.platform(),'machine':platform.machine()}))"]
    runtime = subprocess.run(runtime_command, env=env, text=True, capture_output=True, timeout=args.timeout, check=True)
    report = {"runtime": json.loads(runtime.stdout), "validated_runtime": manifest["validated_runtime"],
              "before_integrity": before, "results": []}
    python = report["runtime"]["executable"]
    for case in manifest["cases"]:
        private = root / "evaluator-only" / case["id"]
        selections = [("existing", root / "cases" / case["id"] / "input", [case["existing_test_module"]])]
        selections.extend((state, private / state, case["gold_tests"]) for state in ("buggy", "fixed"))
        for state, cwd, tests in selections:
            command = [python, "-m", "unittest", "-v", *tests]
            start = time.monotonic()
            error = None
            try:
                proc = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT, text=True, timeout=args.timeout)
                code, text = proc.returncode, proc.stdout
            except subprocess.TimeoutExpired as exc:
                code, text, error = None, exc.stdout or b"", "timeout"
                if isinstance(text, bytes):
                    text = text.decode("utf-8", errors="replace")
            counts = summary(text)
            expected = (case["buggy_expected"] if state == "buggy" else
                        {"tests": case["existing_tests"] if state == "existing" else len(tests),
                         "failures": 0, "errors": 0,
                         "skipped": case["existing_skipped"] if state == "existing" else 0})
            valid = counts["completed"] and code == (1 if state == "buggy" else 0)
            valid = valid and all(counts[key] == value for key, value in expected.items())
            if state == "buggy":
                valid = valid and all(marker in text for marker in case["buggy_failure_markers"])
            elif state == "fixed":
                valid = valid and counts["skipped"] == 0
            filename = case["id"] + "-" + state + ".log"
            (output / filename).write_text(text, encoding="utf-8")
            result = {"case": case["id"], "state": state, "command": command, "cwd": str(cwd),
                      "exit_code": code, "elapsed_seconds": round(time.monotonic() - start, 3),
                      "summary": counts, "expected": expected, "matches_expected": bool(valid),
                      "error": error, "log": filename}
            report["results"].append(result)
            print(case["id"], state, "EXPECTED" if valid else "MISMATCH", counts)
    report["after_integrity"] = {case["id"]: integrity(root, case) for case in manifest["cases"]}
    report["passed"] = all(result["matches_expected"] for result in report["results"]) and all(
        all(states.values()) for states in report["after_integrity"].values())
    write_json(output / "verification.json", report)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
