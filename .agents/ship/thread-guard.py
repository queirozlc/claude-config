#!/usr/bin/env python3
"""Thread guard: one Maestri Chat thread color per ticket.

A ledger names its thread in the head (`Thread: pink`). `maestri say` posts to the thread the
person is in (the `*` in `maestri recall list`); the CLI cannot pick another one. So:

PreToolUse (Bash): a `maestri say` tagged `SHIP_TICKET=<key>` is denied when the person is not in
that ticket's thread. The reply goes to `state/<project>/<key>-outbox.md` instead. An untagged
`maestri say` is denied when the person is in a thread that a ticket owns: tag it with the key, or
with `SHIP_TICKET=none` for a reply that is not about a ticket.

UserPromptSubmit: a message from thread X gets the outbox of the ticket that owns X as context, so
the agent sends it there.

Any failure exits 0: a hook must never wedge a session.
"""
import json, os, re, subprocess, sys

SAY = re.compile(r"(?:^|&&|\|\||;|\|)\s*(?:\w+=\S*\s+)*maestri say\b")
TAG = re.compile(r"\bSHIP_TICKET=([\w#.-]+)")
HEADER = re.compile(r"Below is a message from the user through Maestri Chat\..*?^thread:\s*(\w+)", re.S | re.M)


def threads(cwd):
    """(state folder, open ledgers that name a thread) of the checkout in cwd."""
    import ledger                               # ledger.py, beside this file: the one reader of ledgers
    project = ledger.ship_project(cwd)
    state = os.path.join(ledger.SHIP, "state", project or "")
    if not project or not os.path.isdir(state):
        return None, []
    return state, [l for l in ledger.ledgers(state)[0] if l["open"] and l["thread"]]


def current_thread():
    """The thread the person is in, from `maestri recall list`. Empty when it cannot be told."""
    try:
        out = subprocess.run(["maestri", "recall", "list"], capture_output=True, text=True, timeout=5).stdout
    except Exception:
        return ""
    found = re.search(r"^\*\s+(\w+)", out, re.M)
    return found.group(1).lower() if found else ""


def outbox(state, key):
    return os.path.join(state, f"{key}-outbox.md")


def check_say(command, state, owned, here):
    """Deny reason for a `maestri say`, or None to allow."""
    tag = TAG.search(command)
    owner = next((l for l in owned if l["thread"] == here), None)
    if not tag:
        if not owner:
            return None
        return (f"The person is in the {here} thread, which belongs to {owner['key']}. Tag the reply: "
                f"`SHIP_TICKET={owner['key']} maestri say ...` when it is about {owner['key']}, "
                "`SHIP_TICKET=<other key>` for another ticket, `SHIP_TICKET=none` when it is about no ticket.")
    key = tag.group(1)
    if key.lower() == "none":
        return None
    target = next((l for l in owned if l["key"] == key), None)
    if not target or target["thread"] == here:
        return None
    box = outbox(state, key)
    return (f"{key} lives in the {target['thread']} thread, but the person is in {here}. `maestri say` can only "
            f"post to {here}. Do not post the {key} reply here. Append it to {box} as `## HH:MM` plus the text; "
            f"it goes out when the person writes in {target['thread']}. In {here} you may send one line that "
            f"names no detail, tagged SHIP_TICKET=none: \"{key} update is waiting in {target['thread']}\".")


def pending(prompt, state, owned):
    """Context for a message from thread X: the outbox of the ticket that owns X."""
    header = HEADER.search(prompt)
    if not header:
        return None
    color = header.group(1).lower()
    notes = []
    for l in owned:
        box = outbox(state, l["key"])
        if l["thread"] == color and os.path.isfile(box) and open(box, errors="ignore").read().strip():
            notes.append(f"{l['key']} has replies waiting for the {color} thread in {box}. Send them first with "
                         f"`SHIP_TICKET={l['key']} maestri say --file {box}`, then delete the file.")
    elsewhere = [f"{l['key']} → {l['thread']}" for l in owned if l["thread"] != color]
    if elsewhere:
        notes.append(f"This message is from {color}. Ticket threads: {', '.join(elsewhere)}. "
                     "Tag every `maestri say` with SHIP_TICKET.")
    return "\n".join(notes) or None


def main():
    ev = json.load(sys.stdin)
    state, owned = threads(ev.get("cwd") or os.getcwd())
    if not owned:
        return
    if ev.get("hook_event_name") == "UserPromptSubmit":
        context = pending(ev.get("prompt", ""), state, owned)
        if context:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit", "additionalContext": context}}))
        return
    command = (ev.get("tool_input") or {}).get("command", "")
    if ev.get("tool_name") != "Bash" or not SAY.search(command):
        return
    here = current_thread()
    if not here:
        return
    reason = check_say(command, state, owned, here)
    if reason:
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny", "permissionDecisionReason": reason}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
