#!/usr/bin/env python3
"""Stop hook: refuse to end a turn with a stale ship ledger.

Blocks only when an open ledger exists for this repo AND the transcript shows a
cycle event (maestri ask, git commit, git push, gh pr) after the ledger's last
write. Silent everywhere else. Any failure exits 0: a hook must never wedge a
session.
"""
import json, os, re, subprocess, sys
from datetime import datetime, timezone

# A trigger counts only at a shell command boundary. Newline is deliberately not
# a boundary: a heredoc body that merely mentions `maestri ask` (editing the ship
# skill, say) is text, not a cycle event.
TRIGGER = re.compile(r"(?:^|&&|\|\||;|\|)\s*(?:maestri ask|git commit|git push|gh pr)\b")
LEDGER = re.compile(r"^[A-Z]{2,10}-\d+\.md$")


def main():
    ev = json.load(sys.stdin)
    if ev.get("stop_hook_active"):          # already blocked once, do not loop
        return
    cwd = ev.get("cwd") or os.getcwd()
    top = subprocess.run(["git", "-C", cwd, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if not top:
        return
    state = os.path.expanduser(f"~/.agents/ship/state/{os.path.basename(top)}")
    if not os.path.isdir(state):
        return

    stale = []
    for name in sorted(os.listdir(state)):
        if not LEDGER.match(name):
            continue
        path = os.path.join(state, name)
        head = open(path).read(400)
        phase = re.search(r"^-?\s*Phase:\s*(.+)$", head, re.M)
        if not phase or phase.group(1).strip().startswith("done"):
            continue
        if worked_since(ev.get("transcript_path"), os.path.getmtime(path)):
            stale.append((name, path, phase.group(1).strip()))

    if not stale:
        return
    lines = "\n".join(f"- {name} (Phase: {phase}) → {path}"
                      for name, path, phase in stale)
    print(json.dumps({"decision": "block", "reason": (
        "Ship ledger is stale. You ran a cycle event after its last write.\n"
        f"{lines}\n"
        "Append one `- HH:MM <what happened>` line to the ## Log, update the "
        "head only if a field changed, then stop. Do not rewrite the log.")}))


def worked_since(transcript, mtime):
    """True if a Bash cycle-event tool call ran after the ledger's last write."""
    if not transcript or not os.path.isfile(transcript):
        return False
    for line in open(transcript, errors="ignore"):
        try:
            ev = json.loads(line)
            when = datetime.fromisoformat(ev["timestamp"].replace("Z", "+00:00"))
        except Exception:
            continue
        if when.timestamp() <= mtime:
            continue
        content = ev.get("message", {}).get("content") or []
        for block in content if isinstance(content, list) else []:
            if not isinstance(block, dict) or block.get("name") != "Bash":
                continue
            if TRIGGER.search(block.get("input", {}).get("command", "")):
                return True
    return False


try:
    main()
except Exception:
    pass
