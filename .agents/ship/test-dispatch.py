#!/usr/bin/env python3
"""Checks for dispatch.py. Run: python3 test-dispatch.py"""
import contextlib
import importlib.util
import io
import tempfile
import time
from pathlib import Path

spec = importlib.util.spec_from_file_location("dispatch", Path(__file__).with_name("dispatch.py"))
dispatch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dispatch)
dispatch.POLL_S = 0.1
dispatch.SETTLE_S = 0.3


def run(tmp, command, timeout_min=1):
    report = Path(tmp) / "report.md"
    argv = ["--out", f"{tmp}/out", "--report", str(report), "--timeout-min", str(timeout_min), "--", *command]
    started = time.time()
    return dispatch.main(argv), time.time() - started, report


with tempfile.TemporaryDirectory() as tmp:
    code, seconds, _ = run(tmp, ["sh", "-c", f"echo done > {tmp}/report.md; sleep 30"])
    assert code == 0 and seconds < 5, "a written report ends the wait while the command hangs"

with tempfile.TemporaryDirectory() as tmp:
    Path(tmp, "report.md").write_text("old round")
    time.sleep(1.2)
    code, _, _ = run(tmp, ["sleep", "30"], timeout_min=0.02)
    assert code == 2, "a report from before the dispatch does not count"

with tempfile.TemporaryDirectory() as tmp:
    code, _, _ = run(tmp, ["sh", "-c", "echo reply; exit 0"])
    assert code == 0 and Path(tmp, "out").read_text() == "reply\n", "a command that returns ends the wait"

with tempfile.TemporaryDirectory() as tmp:
    dispatch.SETTLE_S = 60
    with contextlib.redirect_stdout(io.StringIO()) as printed:
        run(tmp, ["sh", "-c", f"echo done > {tmp}/report.md"])
    dispatch.SETTLE_S = 0.3
    assert "no report yet" not in printed.getvalue(), "a fresh report is not missing when the command returns"

with tempfile.TemporaryDirectory() as tmp:
    code, _, _ = run(tmp, ["sh", "-c", "exit 3"])
    assert code == 3, "a failed command gives its exit code"

print("ok")
