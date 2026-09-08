"""Behavior checks for the optional native-command evidence helper."""

import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import unittest


SCRIPT = (Path(__file__).resolve().parents[1]
          / "plugins/lazyest-qa/skills/lazyest-qa/scripts/run_check.py")


class RunCheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def run_command(self, command, timeout="10"):
        completed = subprocess.run(
            [sys.executable, str(SCRIPT), "--out-dir", str(self.root / "logs"),
             "--cwd", str(self.root), "--timeout", timeout, "--", *command],
            capture_output=True, text=True, timeout=12,
        )
        return completed, json.loads(completed.stdout)

    def test_native_zero_exit_is_not_a_test_verdict(self):
        completed, result = self.run_command([
            sys.executable, "-c",
            "import os,sys; print(os.getcwd()); print('Ran 0 tests', file=sys.stderr)",
        ])
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(result["status"], "completed")
        self.assertEqual(result["command_exit_code"], 0)
        self.assertIn(str(self.root), result["tail"])
        self.assertIn("Ran 0 tests", result["tail"])
        self.assertNotIn("PASS", completed.stdout)
        self.assertEqual(result["tail"], Path(result["log_path"]).read_text())

    def test_literal_argv_no_shell_expansion(self):
        literal = "$(touch injected); `touch another` $HOME *"
        completed, result = self.run_command([
            sys.executable, "-c", "import sys; print(sys.argv[1])", literal,
        ])
        self.assertEqual(completed.returncode, 0)
        self.assertEqual(result["tail"].strip(), literal)
        self.assertFalse((self.root / "injected").exists())
        self.assertFalse((self.root / "another").exists())

    def test_first_failure_log_survives_successful_retry_and_tail_is_bounded(self):
        first, failure = self.run_command([
            sys.executable, "-c",
            "import sys; print('FIRST FAILURE'); print('가' * 50000); "
            "print('END', file=sys.stderr); sys.exit(7)",
        ])
        original = Path(failure["log_path"]).read_bytes()
        second, retry = self.run_command([sys.executable, "-c", "print('retry completed')"])
        self.assertEqual(first.returncode, 7)
        self.assertEqual(failure["command_exit_code"], 7)
        self.assertEqual(second.returncode, 0)
        self.assertNotEqual(failure["log_path"], retry["log_path"])
        self.assertEqual(original, Path(failure["log_path"]).read_bytes())
        self.assertIn(b"FIRST FAILURE", original)
        self.assertIn(b"END", original)
        self.assertEqual(len(failure["tail"]), 2000)
        self.assertGreater(failure["log_bytes"], 100000)

    def test_missing_executable_has_127_and_preserves_log(self):
        completed, result = self.run_command([str(self.root / "missing-command")])
        self.assertEqual(completed.returncode, 127)
        self.assertEqual(result["status"], "not_found")
        self.assertIsNone(result["command_exit_code"])
        self.assertTrue(Path(result["log_path"]).is_file())

    @unittest.skipUnless(os.name == "posix", "POSIX execute permission")
    def test_unexecutable_file_has_126(self):
        command = self.root / "not-executable"
        command.write_text("#!/bin/sh\nexit 0\n")
        command.chmod(0o600)
        completed, result = self.run_command([str(command)])
        self.assertEqual(completed.returncode, 126)
        self.assertEqual(result["status"], "cannot_execute")
        self.assertIsNone(result["command_exit_code"])

    def test_log_setup_failure_has_125_and_does_not_run_command(self):
        (self.root / "logs").write_text("occupied")
        completed, result = self.run_command([
            sys.executable, "-c", "from pathlib import Path; Path('executed').touch()",
        ])
        self.assertEqual(completed.returncode, 125)
        self.assertEqual(result["status"], "setup_error")
        self.assertIsNone(result["log_path"])
        self.assertFalse((self.root / "executed").exists())

    def test_timeout_retains_prior_output(self):
        completed, result = self.run_command([
            sys.executable, "-u", "-c", "import time; print('before timeout'); time.sleep(30)",
        ], timeout="0.2")
        self.assertEqual(completed.returncode, 124)
        self.assertEqual(result["status"], "timeout")
        self.assertIsNotNone(result["command_exit_code"])
        self.assertIn("before timeout", result["tail"])
        self.assertLess(result["elapsed_seconds"], 6)

    @unittest.skipUnless(os.name == "posix", "POSIX group cleanup")
    def test_timeout_stops_descendant_that_ignores_termination(self):
        heartbeat = self.root / "heartbeat"
        child = (
            "import signal,time; from pathlib import Path; "
            "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
            f"p=Path({str(heartbeat)!r}); "
            "exec('while True:\\n p.write_text(str(time.time_ns()))\\n time.sleep(0.02)')"
        )
        parent = (
            "import subprocess,sys,time; "
            f"child=subprocess.Popen([sys.executable,'-c',{child!r}]); "
            "print(child.pid, flush=True); time.sleep(30)"
        )
        completed, result = self.run_command([sys.executable, "-c", parent], timeout="0.5")
        self.assertEqual(completed.returncode, 124)
        self.assertTrue(heartbeat.exists())
        time.sleep(0.1)
        stopped_value = heartbeat.read_text()
        time.sleep(0.2)
        self.assertEqual(heartbeat.read_text(), stopped_value)

    @unittest.skipUnless(os.name == "posix", "POSIX signal exit status")
    def test_signal_status_is_recorded_and_mapped_for_shell_exit(self):
        completed, result = self.run_command([
            sys.executable, "-c", "import os,signal; os.kill(os.getpid(), signal.SIGTERM)",
        ])
        self.assertEqual(result["command_exit_code"], -signal.SIGTERM)
        self.assertEqual(completed.returncode, 128 + signal.SIGTERM)


if __name__ == "__main__":
    unittest.main()
