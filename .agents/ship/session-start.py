#!/usr/bin/env python3
"""SessionStart hook (startup, resume, clear, compact): the resume card.

Prints, for a Maestro in a ship checkout, one card of about 3k characters:
the head of every open ledger it owns (with its Reminders line), the hard
rules, and the files to read for the phase. Seats and checkouts without a
ship project get nothing. Any failure exits 0: a hook never wedges a session.
"""
import json, os, re, sys

HARD_RULES = """## Hard rules (hold even before you read the files)
1. A Maestri Chat message gets its reply only through `maestri say`, in its thread. Terminal text does not reach Lucas
2. No commit, push, Jira move or issue, Slack post, GitHub reply or merge without Lucas's explicit OK for that action. Bot threads are the one exception
3. Gate order: Test Plan, evidence per case on a real environment, proof file `Validated at: <head sha>`, then the commit request. Spec output or a log is never evidence
4. A reviewer thread starts with `Kind: question | suggestion | change request`. A question gets a reply, never a fix option. Before any option that widens the PR, search Slack and Jira for the ticket that owns it
5. Every fact has a source (file:line, doc, real run). Never invent a reason. An unverified seat finding stays out of a reply
6. Ask Lucas only for a product or money rule with no precedent, an action that is hard to undo or that others see, or access only he has. One decision per message. Decide the rest and log it
7. Every work message to a seat goes through dispatch.py, in the background, after the seat prep. `maestri check` before you say a seat is working
8. One ledger log line after every cycle event. Every "tell Lucas later" goes in the head's `Reminders:` line, nothing else survives a clear. Only the floor Maestro posts `maestri floor status`
9. Never create tracker tickets. Never merge
10. Replies to Lucas: short, answer first, story before code, his voice in every text others read (`house/talking-to-lucas.md`, `enerflo-shared/ticket-artifacts.md` Writing style)"""

SKILL = os.path.expanduser("~/.claude/skills/ship/references")
HOUSE = os.path.expanduser("~/.agents/ship/house")
FILES = {
    "0": ["floor.md", "team.md", "dispatch.md"],
    "1": ["cycle.md", "dispatch.md"],
    "2": ["cycle.md", "dispatch.md"],
    "3": ["cycle.md", "team.md", "dispatch.md"],
    "4": ["dispatch.md", "cycle.md"],
    "5": ["cycle.md", "dispatch.md"],
    "6": ["cycle.md", "state.md"],
}
FIELDS = ["Phase", "Floor", "Maestro", "Master", "Thread", "Branch", "PR", "Ticket", "Next", "Open", "Reminders", "Seats"]


def head_lines(path):
    with open(path, errors="ignore") as f:
        head = f.read(4000).split("\n## Log", 1)[0]
    out = []
    for label in FIELDS:
        m = re.search(rf"^-?[ \t]*{label}:[ \t]*(.+)$", head, re.M)
        if m:
            out.append(f"{label}: {m.group(1).strip()[:300]}")
    return out


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import ledger
    ev = json.load(sys.stdin)
    cwd = ev.get("cwd") or os.getcwd()
    scan = ledger.scan(cwd)
    if not scan["project"] or scan["seat"]:
        return
    source = ev.get("source", "startup")
    card = [f"# Ship resume card ({source}, project {scan['project']})"]
    if scan["ledgers"]:
        card.append("## Open ledgers you own")
        for l in scan["ledgers"]:
            tag = " (routed: append log lines only)" if l.get("routed") else ""
            card.append(f"### {l['key']}{tag}\n{l['path']}")
            card += head_lines(l["path"])
        phases = {l["phase"][:1] for l in scan["ledgers"]}
        files = []
        for p in sorted(phases):
            files += [f for f in FILES.get(p, ["cycle.md"]) if f not in files]
        card.append("## Read before the first action")
        card.append(f"- `{HOUSE}/maestro.md`, then `{HOUSE}/talking-to-lucas.md` before the first reply to Lucas")
        card.append("- " + ", ".join(f"`{SKILL}/{f}`" for f in files) + " (the references for the current phase; the others on their condition)")
        card.append("- Load the `maestri-manager` and `maestri-workspace` skills. Review ledgers also need `review.md` and `review-briefs.md`")
    else:
        card.append("No open ledger for this checkout. `/ship <KEY>` starts one; read `floor.md`, `team.md`, `cycle.md` then.")
    if scan["paused"]:
        card.append("Paused: " + ", ".join(scan["paused"]))
    if scan["problems"]:
        card.append("Ledger problems: " + " | ".join(scan["problems"]))
    card.append(HARD_RULES)
    print("\n".join(card)[:6000])


try:
    main()
except Exception:
    pass
