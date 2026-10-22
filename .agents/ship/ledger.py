#!/usr/bin/env python3
"""The one reader of ship cycle ledgers.

The Stop hooks import it. The Claude Code mods (ship-guard, context-handoff) and agents run it:

    ledger.py [cwd]    JSON: the open ledgers that belong to the agent in cwd, and every problem

A ledger whose Phase starts with `paused` is not open: no mod and no Stop hook acts on it. Its key
is listed in `paused`.

Contract, as references/state.md of the ship skill states it: a ledger is a `.md` file directly in
~/.agents/ship/state/<project>/ whose head (the text above `## Log`) has a `# <key> — cycle state`
title and a `Phase:` line. The file name is not checked, so every ticket key form works.
"""
import json, os, re, subprocess, sys

SHIP = os.path.expanduser("~/.agents/ship")
FINISHED = re.compile(r"(?:\d+-)?(?:done|closed|merged)\b")
PAUSED = re.compile(r"paused\b", re.I)
FLOORS = "/.maestri/floors/"


def field(head, label):
    found = re.search(rf"^-?[ \t]*{label}:[ \t]*(.+)$", head, re.M)
    return found.group(1).strip() if found else ""


def read(path):
    """(ledger, problem) of one state file. Both None: the file is not a ledger."""
    with open(path, errors="ignore") as f:
        head = f.read(4000).split("\n## Log", 1)[0]
    name = os.path.basename(path)
    titled = re.search(r"^# .*cycle state", head, re.M | re.I)
    phase = field(head, "Phase")
    if not titled and not phase:
        return None, None
    if not titled:
        return None, f"{name} has a Phase line but no `# <key> — cycle state` title. It is not read as a ledger."
    if not phase:
        return None, f"{name} has a cycle state title but no `Phase:` line. It is not read as a ledger."
    paused = bool(PAUSED.match(phase))
    return {
        "key": name[:-3], "path": path, "phase": phase, "paused": paused,
        "open": not paused and not FINISHED.match(phase),
        "floor": field(head, "Floor"), "maestro": field(head, "Maestro"), "master": field(head, "Master"),
        "branch": (field(head, "Branch").split() or [""])[0], "next": field(head, r"Next(?: action)?"),
        "thread": (field(head, "Thread").lower().replace("none", "").split() or [""])[0],
        "mtimeMs": os.path.getmtime(path) * 1000,
    }, None


def ledgers(state):
    """Every ledger of a state folder, and the problems of the files that fail the contract."""
    found, problems = [], []
    for name in sorted(os.listdir(state)):
        path = os.path.join(state, name)
        if not name.endswith(".md") or not os.path.isfile(path):
            continue
        ledger, problem = read(path)
        if ledger:
            found.append(ledger)
        if problem:
            problems.append(problem)
    return found, problems


def git(cwd, *args):
    return subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True).stdout.strip()


def checkout(cwd):
    """(top, main): this checkout and the main checkout. A linked worktree can have any folder name."""
    top = git(cwd, "rev-parse", "--show-toplevel")
    main = git(cwd, "worktree", "list", "--porcelain").split("\n", 1)[0].removeprefix("worktree ")
    return top, main or top


def ship_project(cwd):
    """The ship project of the checkout: its CLAUDE.local.md link target, else the main checkout name."""
    top, main = checkout(cwd)
    if not top:
        return None
    link = os.path.join(top, "CLAUDE.local.md")
    if os.path.islink(link):
        target = os.path.realpath(link)
        if os.path.dirname(os.path.dirname(target)) == os.path.realpath(SHIP):
            return os.path.basename(os.path.dirname(target))
    name = os.path.basename(main)
    # A floor made as a clone is its own main checkout. Maestri names it <ground folder>--<branch>.
    if FLOORS in os.path.realpath(top) + "/" and os.path.realpath(top) == os.path.realpath(main):
        name = name.split("--", 1)[0]
    return name or None


def is_seat(cwd):
    """A recruit with a role starts in <checkout>/.maestri/roles/<id>. Only a Maestro role runs a cycle."""
    role_dir = re.match(r".*/\.maestri/roles/[^/]+", cwd + "/")
    if not role_dir:
        return False
    try:
        with open(os.path.join(role_dir.group(0), "role.json")) as f:
            role = json.load(f).get("name", "")
    except Exception:
        role = ""
    return not re.search("maestro", role, re.I)


def mine(found, floor, branch):
    """The ledgers of this agent. The ground Maestro runs or routes every cycle of the project.
    A floor Maestro has the ledger that names its floor folder or its branch."""
    if floor is None:
        return found
    return [l for l in found if floor in l["floor"] or (branch and l["branch"] == branch)]


def scan(cwd):
    """What the agent in cwd must know: its open ledgers and the problems that hide a ledger."""
    out = {"project": None, "seat": False, "floor": None, "branch": "", "ledgers": [], "paused": [], "problems": []}
    project = ship_project(cwd)
    state = os.path.join(SHIP, "state", project or "")
    if not project or not os.path.isdir(state):
        return out
    out["project"] = project
    out["seat"] = is_seat(cwd)
    if out["seat"]:
        return out
    top, main = checkout(cwd)
    if FLOORS in os.path.realpath(cwd) + "/" or os.path.realpath(top) != os.path.realpath(main):
        out["floor"] = os.path.basename(top)
    found, out["problems"] = ledgers(state)
    out["branch"] = git(cwd, "branch", "--show-current")
    own = mine(found, out["floor"], out["branch"])
    for l in own:
        # On the ground, a ledger with a clone path in Floor is a floor cycle: the ground Maestro routes it.
        l["routed"] = out["floor"] is None and "/" in l["floor"]
    out["ledgers"] = [l for l in own if l["open"]]
    out["paused"] = [l["key"] for l in own if l["paused"]]
    return out


if __name__ == "__main__":
    print(json.dumps(scan(os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.getcwd()))))
