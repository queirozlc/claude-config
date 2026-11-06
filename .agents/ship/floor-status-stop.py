#!/usr/bin/env python3
"""Stop hook: ask for a Maestri floor status post after a turn that did work.

Blocks only when this terminal runs on a floor (not the ground level) in
Maestri, it is not a seat (a recruit whose role is not a Maestro), `maestri floor status` answers for it, and the transcript shows work in the current turn (an edit, a write, a
sub-agent, a cycle event or a deploy) with no `maestri floor status "<text>"` post. The
reason carries the current status, so a turn with no news re-posts the same
line. Silent everywhere else. Any failure exits 0: a hook must never wedge a
session.

On the ground level, the ground Maestro does floor work too (deploy, live test).
There it blocks when the turn wrote the ledger of a floor cycle and did not post
`maestri floor status --floor "<floor>" "<text>"` for that floor.
"""
import json, os, re, shlex, subprocess, sys
from datetime import datetime

# A command boundary. ` -- ` covers `dispatch.py ... -- maestri ask`. Newline is not a
# boundary: a heredoc body that merely mentions a cycle event is text.
BOUNDARY = r"(?:^|&&|\|\||;|\||\s--\s)\s*"
# Same cycle events as ledger-stop.py.
TRIGGER = re.compile(BOUNDARY + r"(?:maestri ask|git(?:\s+-C\s+\S+)?\s+(?:commit|push)|gh pr|(?:pnpm |npx )?cdk deploy)\b")
STATUS = re.compile(r"(?:\S*/)?(?:maestri|\$\{?MAESTRI_CLI\}?|\"\$\{?MAESTRI_CLI\}?\")\s+floor\s+status\b")
WORK_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit", "Task", "Agent"}
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}


def status_posts(command):
    """Every `maestri floor status` call in the command that carries a text: its --floor
    value, or None for the terminal's own floor. Flag order does not matter."""
    for segment in re.split(r"&&|\|\||;|\|", command):
        segment = segment.strip()
        if not STATUS.match(segment):
            continue
        try:
            args = shlex.split(segment)[3:]
        except ValueError:
            continue
        floor, text, i = None, False, 0
        while i < len(args):
            arg = args[i]
            if arg == "--floor" and i + 1 < len(args):
                floor, i = args[i + 1], i + 2
            elif arg in ("--state", "--progress") and i + 1 < len(args):
                i += 2
            elif arg.startswith("--"):
                i += 1
            else:
                text, i = True, i + 1
        if text:
            yield floor


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
    if current is None:
        return
    turn = this_turn(ev.get("transcript_path"))
    if not on_floor(cwd, current):
        return ground_check(cwd, turn)
    stale = [l for l in ledger.scan(cwd)["ledgers"] if wrong_state(l, current)]
    if stale:
        print(json.dumps({"decision": "block", "reason": (
            f"{stale[0]['key']}: the PR is ready for review, but the sidebar says working:\n  {current}\n"
            'Post it again with the review state: `maestri floor status "<your agent name>: <where the work stands now>" '
            "--state review`. Review is how Lucas learns the PR waits on reviewers. Then stop.")}))
        return
    if not turn["work"] or turn["posted"]:
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


def ground_check(cwd, turn):
    """Block when this turn wrote an open floor ledger and posted nothing for that floor."""
    import ledger
    project = ledger.ship_project(cwd)
    state = os.path.join(ledger.SHIP, "state", project or "")
    if not project or not os.path.isdir(state):
        return
    found, _ = ledger.ledgers(state)
    written = {l["floor"].split(" · ")[0]: l for l in found
               if l["open"] and " · " in l["floor"] and l["mtimeMs"] >= turn["start"]
               and not l.get("routedFrom") and wrote(l["key"], turn["calls"])}
    # A floor of another workspace: `maestri floor status --floor` cannot reach it from here.
    written = {f: l for f, l in written.items() if floor_status(f) is not None}
    shown = lambda s: re.sub(r'^"[^"]*":\s*|\s+·\s+by\s.*$', "", s or "(no status)")
    stale = [f for f, l in written.items() if f in turn["floors"] and wrong_state(l, floor_status(f))]
    if stale:
        lines = "\n".join(f"  {f}: {shown(floor_status(f))}" for f in stale)
        print(json.dumps({"decision": "block", "reason": (
            f"The PR of these floors is ready for review, but the sidebar says working:\n{lines}\n"
            'Post again with `maestri floor status --floor "<floor>" "<your agent name>: <where the work stands now>" '
            "--state review`. Then stop.")}))
        return
    missing = [f for f in written if f not in turn["floors"]]
    if not missing:
        return
    lines = "\n".join(f"  {f}: {shown(floor_status(f))}" for f in missing)
    print(json.dumps({"decision": "block", "reason": (
        "Floor status not posted this turn. You wrote the ledger of a floor cycle, and its sidebar shows:\n"
        f"{lines}\n"
        'Run `maestri floor status --floor "<floor>" "<your agent name>: <where the work stands now>"` '
        "for each floor, with `--state review|blocked|done` when that is the state. Then stop.")}))


def wrong_state(l, status):
    """A PR out of draft (`PR: <url> (ready for review)`) belongs in review, not working."""
    state = re.match(r'^"[^"]*":\s*\[(\w+)', status or "")
    ready = re.search(r"\bready\b", l.get("pr", ""), re.I) and not re.search(r"\bdraft\b", l.get("pr", ""), re.I)
    return bool(ready and l["phase"] in ("6-pr-open", "6-awaiting-merge-permission")
                and state and state.group(1) == "working")


def wrote(key, calls):
    """The turn wrote the ledger file: an edit tool on it, or a Bash command that redirects
    or copies into it. A command that only reads it (cat, grep, sed -n, tail) does not count,
    even when another agent changed the file during the turn."""
    name = rf"(?<![\w-]){re.escape(key)}\.md\b"
    writer = re.compile(r"(?:>>?|\btee\b|\bsed\s+-i\S*|\bperl\s+-p?i\S*|\bmv\b|\bcp\b)[^|;&\n]*" + name)
    for tool, text in calls:
        if tool in EDIT_TOOLS and re.search(name, text):
            return True
        if tool == "Bash" and writer.search(text):
            return True
    return False


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


def new_turn(timestamp=""):
    try:
        start = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).timestamp() * 1000
    except Exception:
        start = 0
    return {"work": 0, "posted": 0, "floors": set(), "calls": [], "start": start}


def this_turn(transcript):
    """What the turn did since the last real user prompt of the transcript: work and posts
    (counts), floors posted with --floor, (tool, command or file path) calls, start time (ms)."""
    turn = new_turn()
    if not transcript or not os.path.isfile(transcript):
        return turn
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
            turn = new_turn(ev.get("timestamp", ""))
            continue
        for b in blocks:
            if not isinstance(b, dict) or b.get("type") != "tool_use":
                continue
            given = b.get("input") or {}
            command = given.get("command", "") if b.get("name") == "Bash" else ""
            turn["calls"].append((b.get("name"), command or str(given.get("file_path", ""))))
            posts = list(status_posts(command))
            for floor in posts:
                if floor is None:
                    turn["posted"] += 1
                else:
                    turn["floors"].add(floor)
            if not posts and (b.get("name") in WORK_TOOLS or TRIGGER.search(command)):
                turn["work"] += 1
    return turn


try:
    main()
except Exception:
    pass
