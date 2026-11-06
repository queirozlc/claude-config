#!/usr/bin/env python3
"""Write per-seat MCP deny lists into ~/.claude.json.

    apply.py <checkout>        checkout root gets the maestro profile; every
                               .maestri/roles/<id> under it gets the profile
                               of its role name. On a floor, role dirs that
                               sibling floors of the same project already
                               have are pre-written, so a seat recruited later
                               starts with its profile.
    apply.py --dry-run <checkout>

Profiles: ~/.agents/ship/mcp/profiles.json. Claude Code reads
`projects.<dir>.disabledMcpServers` at start, so a running seat changes on
its next restart.
"""
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE_JSON = os.path.expanduser("~/.claude.json")


def load_profiles():
    with open(os.path.join(HERE, "profiles.json")) as fh:
        return json.load(fh)


def seat_type(role_name, profiles):
    for word, seat in profiles["roles"]:
        if word.lower() in role_name.lower():
            return seat
    return None


def role_dirs(checkout):
    """(dir, role name) for every role dir under checkout, plus the ones
    sibling floors of the same project already have."""
    found = {}
    for f in glob.glob(os.path.join(checkout, ".maestri", "roles", "*", "role.json")):
        found[os.path.dirname(f)] = role_name(f)

    floors_dir = os.path.dirname(checkout)
    if os.path.basename(floors_dir) == "floors" and os.path.basename(os.path.dirname(floors_dir)) == ".maestri":
        project = os.path.basename(checkout).split("--")[0]
        for f in glob.glob(os.path.join(floors_dir, project + "--*", ".maestri", "roles", "*", "role.json")):
            rid = os.path.basename(os.path.dirname(f))
            target = os.path.join(checkout, ".maestri", "roles", rid)
            found.setdefault(target, role_name(f))
    return found


def role_name(path):
    try:
        with open(path) as fh:
            return json.load(fh).get("name", "")
    except (OSError, ValueError):
        return ""


def disabled_for(seat, profiles, existing):
    keep = set(profiles["keep"][seat])
    known = set(profiles["servers"])
    out = [s for s in existing if s not in known]
    out += sorted(s for s in known if s not in keep)
    return out


def main(argv):
    dry = "--dry-run" in argv
    args = [a for a in argv if a != "--dry-run"]
    if len(args) != 1:
        print(__doc__)
        return 1
    checkout = os.path.realpath(os.path.expanduser(args[0]))
    try:
        checkout = subprocess.check_output(
            ["git", "-C", checkout, "rev-parse", "--show-toplevel"], text=True
        ).strip()
    except subprocess.CalledProcessError:
        pass

    profiles = load_profiles()
    plan = {checkout: "maestro"}
    for d, name in role_dirs(checkout).items():
        seat = seat_type(name, profiles)
        if seat is None:
            print(f"skip {d}: no profile for role '{name}'")
            continue
        plan[d] = seat

    with open(CLAUDE_JSON) as fh:
        data = json.load(fh)
    projects = data.setdefault("projects", {})
    for d, seat in plan.items():
        entry = projects.setdefault(d, {})
        new = disabled_for(seat, profiles, entry.get("disabledMcpServers") or [])
        changed = new != (entry.get("disabledMcpServers") or [])
        entry["disabledMcpServers"] = new
        print(f"{'would set' if dry else 'set' if changed else 'kept'} {seat:9s} {d}")

    if dry:
        return 0
    tmp = CLAUDE_JSON + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(data, fh, indent=2)
    os.replace(tmp, CLAUDE_JSON)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
