#!/usr/bin/env python3
"""Run a dispatch and return when its report files are written.

`maestri ask` does not always return when the seat goes idle, so the report
files are the wake signal, not the ask.

    dispatch.py --out <file> --report <file> [--report <file>] \
        [--timeout-min 30] -- maestri ask "<seat>" "<prompt>"

Exit 0: every report is written, or the command returned with 0.
Exit 2: timeout. The command still runs, the seat is not touched.
"""
import argparse
import subprocess
import sys
import time
from pathlib import Path

POLL_S = 5
# A seat writes its report, then ends its turn. Do not wake the Maestro before that.
SETTLE_S = 10


def written(report, start, settled=True):
    try:
        stat = report.stat()
    except FileNotFoundError:
        return False
    settle = SETTLE_S if settled else 0
    return stat.st_size > 0 and start <= stat.st_mtime <= time.time() - settle


def parse(argv):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--report", required=True, type=Path, action="append")
    parser.add_argument("--timeout-min", type=float, default=30)
    parser.add_argument("command", nargs="+")
    return parser.parse_args(argv)


def wait(proc, reports, start, deadline):
    while time.time() < deadline:
        if all(written(report, start) for report in reports):
            return "reports"
        if proc.poll() is not None:
            return "returned"
        time.sleep(POLL_S)
    return "timeout"


def main(argv=None):
    args = parse(argv)
    reports = [report.expanduser() for report in args.report]
    # 1 second of slack for file systems with coarse mtime
    start = time.time() - 1
    with args.out.expanduser().open("w") as out:
        proc = subprocess.Popen(args.command, stdout=out, stderr=subprocess.STDOUT)
        result = wait(proc, reports, start, start + args.timeout_min * 60)
    missing = [str(report) for report in reports if not written(report, start, settled=False)]
    if result == "reports":
        proc.terminate()
        print("reports written:", *map(str, reports), sep="\n  ")
        return 0
    if result == "returned":
        print(f"command returned with exit {proc.returncode}, output in {args.out}")
        if missing:
            print("no report yet:", *missing, sep="\n  ")
        return proc.returncode
    print(f"TIMEOUT after {args.timeout_min:g} min. Do not send the prompt again.")
    print("Run `maestri check` on each seat. No report from:", *missing, sep="\n  ")
    print(f"The command still runs as pid {proc.pid}.")
    return 2


if __name__ == "__main__":
    sys.exit(main())
