#!/usr/bin/env python3
"""Stop hook: ask for a Maestri floor status post after a turn that did work.

Blocks only when this terminal runs on a floor (not the ground level) in
Maestri, it is not a seat (a recruit whose role is not a Maestro), `maestri floor status` answers for it, and the transcript shows work in the current turn (an edit, a write, a
sub-agent, or a cycle event) with no `maestri floor status "<text>"` post. The
reason carries the current status, so a turn with no news re-posts the same
line. Silent everywhere else. Any failure exits 0: a hook must never wedge a
session.
"""
import json, os, re, subprocess, sys

BOUNDARY = r"(?:^|&&|\|\||;|\|)\s*"
# Same cycle events as ledger-stop.py, so a heredoc that merely mentions them is text.
TRIGGER = re.compile(BOUNDARY + r"(?:maestri ask|git commit|git push|gh pr)\b")
POST = re.compile(BOUNDARY + r"maestri floor status\s+[\"']")
WORK_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "Task", "Agent"}


def main():
    ev = json.load(sys.stdin)
    if ev.get("stop_hook_active"):          # already blocked once, do not loop
        return
    if not os.environ.get("MAESTRI_TERMINAL_ID"):
        return
    import ledger                           # ledger.py, beside this file
    cwd = ev.get("cwd") or os.getcwd()
    # One writer per floor: a seat's post replaces the floor Maestro's line in the sidebar.
    if ledger.is_seat(cwd):
        return
    current = floor_status()
    if current is None or not on_floor(cwd, current):
        return
    work, posted = this_turn(ev.get("transcript_path"))
    if not work or posted:
        return
    # The CLI prints `"<floor>": [<state>] <text>  ·  by <agent>`; a new floor says "has no status yet".
    line = re.match(r'^"[^"]*":\s*\[(\w+)(?:\s+(\d+%))?\]\s*(.*?)(?:\s+·\s+by\s.*)?$', current)
    text = "" if "has no status yet" in current else (line.group(3) if line else current)
    # A re-post without the flags resets the sidebar to working with no progress bar.
    flags = ""
    if line and line.group(1) != "working":
        flags += f" --state {line.group(1)}"
    if line and line.group(2):
        flags += f" --progress {line.group(2)}"
    again = f' Nothing changed? Post it again: `maestri floor status "{text}"{flags}`.' if text else ""
    print(json.dumps({"decision": "block", "reason": (
        "Floor status not posted this turn. You did work and the sidebar shows:\n"
        f"  {text or '(empty)'}\n"
        'Run `maestri floor status "<your agent name>: <where the work stands now>"` '
        f"(add `--progress 2/5` when the task has countable steps).{again} "
        "Posting again keeps the sidebar current. You are the only writer on this floor: "
        "seats report to you, and you set blocked, review and done. Then stop.")}))


def on_floor(cwd, own):
    """Floors live in <workspace>/.maestri/floors/<project>--<branch>, as a worktree or a clone.
    A --no-git floor shares the ground directory: there the status differs from Ground's."""
    if "/.maestri/floors/" in os.path.realpath(cwd) + "/":
        return True
    ground = floor_status("Ground")
    return ground is not None and own != ground


def floor_status(floor=None):
    """What `maestri floor status` prints for this terminal's floor (or a named one), None when Maestri cannot answer."""
    cli = os.environ.get("MAESTRI_CLI") or "maestri"
    try:
        out = subprocess.run([cli, "floor", "status", *(["--floor", floor] if floor else [])],
                             capture_output=True, text=True, timeout=5)
    except Exception:
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def this_turn(transcript):
    """(work, posted): counts since the last real user prompt of the transcript."""
    work = posted = 0
    if not transcript or not os.path.isfile(transcript):
        return work, posted
    for line in open(transcript, errors="ignore"):
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("isSidechain"):
            continue
        content = (ev.get("message") or {}).get("content")
        blocks = content if isinstance(content, list) else []
        is_result = any(isinstance(b, dict) and b.get("type") == "tool_result" for b in blocks)
        if ev.get("type") == "user" and not is_result and not ev.get("isMeta"):
            work = posted = 0
            continue
        for b in blocks:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            command = (b.get("input") or {}).get("command", "") if b.get("name") == "Bash" else ""
            if POST.search(command):
                posted += 1
            elif b.get("name") in WORK_TOOLS or TRIGGER.search(command):
                work += 1
    return work, posted


try:
    main()
except Exception:
    pass
