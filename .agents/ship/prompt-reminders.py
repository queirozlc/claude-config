#!/usr/bin/env python3
"""UserPromptSubmit hook: the Reminders lines of the open ledgers, every prompt.

A Maestro in a ship checkout sees `Reminders (<KEY>): <text>` for each open
ledger whose head has a `Reminders:` line, so a "tell Lucas later" survives a
clear and a long turn. Seats, checkouts without a ship project and ledgers
without the line print nothing. Capped at 10k characters. Any failure exits 0.
"""
import json, os, re, sys


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ledger
    ev = json.load(sys.stdin)
    scan = ledger.scan(ev.get("cwd") or os.getcwd())
    if not scan["project"] or scan["seat"]:
        return
    out = []
    for l in scan["ledgers"]:
        with open(l["path"], errors="ignore") as f:
            head = f.read(4000).split("\n## Log", 1)[0]
        m = re.search(r"^-?[ \t]*Reminders:[ \t]*(.+)$", head, re.M)
        text = m.group(1).strip() if m else ""
        if text and text.lower() != "none":
            out.append(f"Reminders ({l['key']}): {text}")
    if out:
        print("\n".join(out)[:10000])


try:
    main()
except Exception:
    pass
