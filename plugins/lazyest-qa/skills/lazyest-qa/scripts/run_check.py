#!/usr/bin/env python3
"""Run one native command and retain its output; does not assess test results.

Python 3.9+. Example: run_check.py --out-dir evidence -- python -m unittest
Exit: native code (signals: 128 + signal), 124 timeout, 125 capture/setup error,
126 cannot execute, 127 command not found, 130 interrupted. No shell is used.
Timeout cleanup covers the POSIX process group; Windows cleanup is best effort.
"""

import argparse
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time


TAIL_CHARS = 2000


def positive_seconds(value):
    seconds = float(value)
    if not math.isfinite(seconds) or seconds <= 0:
        raise argparse.ArgumentTypeError("timeout must be finite and positive")
    return seconds


def stop_processes(process):
    """Allow a short shutdown, then terminate remaining group members."""
    try:
        if os.name == "posix":
            os.killpg(process.pid, signal.SIGTERM)
        else:
            process.send_signal(signal.CTRL_BREAK_EVENT)
    except (ProcessLookupError, OSError):
        pass
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        pass
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    elif process.poll() is None:
        # Without Windows Job Objects, detached descendants cannot be guaranteed.
        try:
            subprocess.run(["taskkill", "/PID", str(process.pid), "/T", "/F"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=5, check=False)
        except (OSError, subprocess.TimeoutExpired):
            pass
        if process.poll() is None:
            process.kill()
    process.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cwd", default=".", help="command working directory")
    parser.add_argument("--out-dir", required=True, help="directory for unique logs")
    parser.add_argument("--timeout", type=positive_seconds, default=120,
                        help="wall-clock seconds before stopping (default: 120)")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if len(args.command) < 2 or args.command[0] != "--":
        parser.error("supply an explicit command after --")
    command = args.command[1:]
    cwd = Path(args.cwd).resolve()
    if not cwd.is_dir():
        parser.error("--cwd must be an existing directory")
    process = None
    log_path = None
    status, code = "setup_error", 125
    started = time.monotonic()
    error = None
    try:
        out_dir = Path(args.out_dir).resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        descriptor, log_path = tempfile.mkstemp(prefix="check-", suffix=".log",
                                               dir=str(out_dir))
        with os.fdopen(descriptor, "wb") as log:
            options = {"start_new_session": True} if os.name == "posix" else {
                "creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
            try:
                process = subprocess.Popen(command, cwd=str(cwd), shell=False,
                                           stdin=subprocess.DEVNULL, stdout=log,
                                           stderr=subprocess.STDOUT, **options)
            except FileNotFoundError as exc:
                status, code, error = "not_found", 127, str(exc)
            except OSError as exc:
                status, code, error = "cannot_execute", 126, str(exc)
            if process is not None:
                try:
                    actual = process.wait(timeout=args.timeout)
                    status, code = "completed", actual if actual >= 0 else 128 - actual
                except subprocess.TimeoutExpired:
                    stop_processes(process)
                    status, code = "timeout", 124
                except KeyboardInterrupt:
                    stop_processes(process)
                    status, code = "interrupted", 130
    except OSError as exc:
        error = str(exc)
        status, code = "setup_error", 125
        if process is not None and process.poll() is None:
            stop_processes(process)
    result = {"status": status, "command_exit_code": process.returncode if process else None,
              "exit_code": code, "elapsed_seconds": round(time.monotonic() - started, 3),
              "log_path": log_path, "tail": ""}
    if log_path:
        try:
            with open(log_path, "rb") as log:
                log.seek(0, os.SEEK_END)
                size = log.tell()
                log.seek(max(0, size - TAIL_CHARS * 4))
                result["tail"] = log.read().decode("utf-8", errors="replace")[-TAIL_CHARS:]
            result["log_bytes"] = size
        except OSError as exc:
            result.update(status="capture_error", exit_code=125)
            code, error = 125, str(exc)
    if error:
        result["error"] = error
    print(json.dumps(result, ensure_ascii=True))
    return code


if __name__ == "__main__":
    sys.exit(main())
