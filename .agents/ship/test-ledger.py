#!/usr/bin/env python3
"""Runnable check for ledger.py and ledger-stop.py: python3 test-ledger.py"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import ledger

tmp = os.path.realpath(tempfile.mkdtemp())
ledger.SHIP = os.path.join(tmp, ".agents", "ship")        # ledger-stop.py below runs with HOME=tmp
state = os.path.join(ledger.SHIP, "state", "proj")
os.makedirs(state)


def write(name, text):
    path = os.path.join(state, name)
    open(path, "w").write(text)
    return path


def head(key, phase="4-execute", floor="Ground", branch="main", master=""):
    first = f"Master: {master}\n--\n" if master else ""
    return f"{first}# {key} — cycle state\n\nPhase: {phase}\nFloor: {floor}\nMaestro: m\nBranch: {branch} (base: main @ abc)\nNext: do x\n\n## Log\n\n- 10:00 Phase: done\n"


def sh(*args, cwd=None):
    subprocess.run(args, cwd=cwd, check=True, capture_output=True)


# Every key form is a ledger: the head decides, not the file name.
for key in ["HOB-154", "9", "537", "PB-A", "gh-12", "feature_x"]:
    got, problem = ledger.read(write(f"{key}.md", head(key)))
    assert got and got["key"] == key and got["open"] and not problem, key
assert ledger.read(write("9.md", head("#9")))[0]["key"] == "9"                      # GitHub title form
bullets = "# PRE-78 — cycle state\n- Phase: 6-awaiting-merge-permission\n- Next action: wait\n"
assert ledger.read(write("PRE-78.md", bullets))[0]["next"] == "wait"

# Finished phases are not open. The log below the head is not read.
for phase, is_open in [("done", False), ("closed", False), ("7-merged", False), ("5-review", True), ("8-shipped-pr-open", True),
                       ("paused (6-gate)", False), ("Paused", False)]:
    assert ledger.read(write("X-1.md", head("X-1", phase)))[0]["open"] is is_open, phase
assert ledger.read(write("X-1.md", head("X-1", "paused (6-gate)")))[0]["paused"] is True
assert ledger.read(write("X-1.md", head("X-1", "5-review")))[0]["paused"] is False

# Sibling files are not ledgers. A half ledger is a problem, never a silent miss.
assert ledger.read(write("9-brief.md", "## Summary\nbrief text\n")) == (None, None)
assert "no `# <key>" in ledger.read(write("T-1.md", "Phase: 4-execute\n"))[1]
assert "no `Phase:`" in ledger.read(write("T-2.md", "# T-2 — cycle state\n\nFloor: Ground\n"))[1]
for name in os.listdir(state):
    os.remove(os.path.join(state, name))

# Ownership: the ground has every ledger, a floor has the one that names its folder or its branch.
a = {"floor": "A · ~/w/.maestri/floors/proj--a", "branch": "feat/a"}
b = {"floor": "B", "branch": "feat/b"}
assert ledger.mine([a, b], None, "main") == [a, b]
assert ledger.mine([a, b], "proj--a", "other") == [a]
assert ledger.mine([a, b], "proj--zzz", "feat/b") == [b]
assert ledger.mine([a, b], "proj--zzz", "") == []

# A real checkout: ground, a worktree floor, a clone floor, a seat and a floor Maestro in role folders.
ws = os.path.join(tmp, "ws")
ground = os.path.join(ws, "proj")
floors = os.path.join(ws, ".maestri", "floors")
os.makedirs(ground)
os.makedirs(floors)
sh("git", "init", "-q", "-b", "main", cwd=ground)
sh("git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", "x", cwd=ground)
worktree = os.path.join(floors, "proj--feat9")
clone = os.path.join(floors, "proj--feat6")
sh("git", "worktree", "add", "-q", "-b", "feat/9", worktree, cwd=ground)
sh("git", "clone", "-q", ground, clone)
sh("git", "switch", "-q", "-c", "feat/6", cwd=clone)
write("9.md", head("#9", floor=f"9 Slack · {worktree}", branch="feat/9", master="Ned"))
write("6.md", head("#6", floor="6 Store", branch="feat/6"))
write("5.md", head("#5", phase="done"))
write("4.md", head("#4", phase="paused (5-review)"))
write("9-brief.md", "## Summary\nPhase 4 of the plan\n")

keys = lambda cwd: [l["key"] for l in ledger.scan(cwd)["ledgers"]]
assert keys(ground) == ["6", "9"] and ledger.scan(ground)["paused"] == ["4"]
assert [l["routed"] for l in ledger.scan(ground)["ledgers"]] == [False, True]
assert keys(worktree) == ["9"] and ledger.scan(worktree)["floor"] == "proj--feat9"
assert keys(clone) == ["6"] and ledger.scan(clone)["project"] == "proj"            # by branch, in a clone
for cwd, role, want in [(ground, "Backend Executor", []), (worktree, "Proj Maestro", ["9"])]:
    seat = os.path.join(cwd, ".maestri", "roles", "0a1b")
    os.makedirs(seat)
    json.dump({"name": role}, open(os.path.join(seat, "role.json"), "w"))
    assert keys(seat) == want and ledger.scan(seat)["seat"] is (not want), role
# A cycle in another repo that this ground routes: `Routed from: proj` puts it in proj's ledgers.
other = os.path.join(ledger.SHIP, "state", "skills")
os.makedirs(other)
open(os.path.join(other, "S-1.md"), "w").write(head("S-1").replace("Maestro: m", "Maestro: m\nRouted from: proj"))
open(os.path.join(other, "S-2.md"), "w").write(head("S-2"))
open(os.path.join(other, "S-3.md"), "w").write("Phase: 4-execute\n")
assert keys(ground) == ["6", "9", "S-1"] and ledger.scan(ground)["ledgers"][2]["routed"] is True
assert not any("S-3" in p for p in ledger.scan(ground)["problems"])                # other folders' problems stay there
assert keys(worktree) == ["9"]                                                      # a floor does not route it
assert [l["key"] for l in ledger.ledgers(other)[0]] == ["S-1", "S-2"]               # its own project still runs it
skills = os.path.join(ws, "skills")
os.makedirs(skills)
sh("git", "init", "-q", "-b", "main", cwd=skills)
assert [(l["key"], l["routed"]) for l in ledger.scan(skills)["ledgers"]] == [("S-1", False), ("S-2", False)]
for name in os.listdir(other):
    os.remove(os.path.join(other, name))
os.rmdir(other)
assert ledger.scan(tmp) == {"project": None, "seat": False, "floor": None, "branch": "", "ledgers": [], "paused": [], "problems": []}

# ledger-stop.py blocks a turn that ran a cycle event after the last write of a number-key ledger.
transcript = os.path.join(tmp, "t.jsonl")
event = {"timestamp": "2099-01-01T00:00:00Z", "message": {"content": [
    {"type": "tool_use", "name": "Bash", "input": {"command": 'maestri ask "Jon 9" "go"'}}]}}
open(transcript, "w").write(json.dumps(event) + "\n")
hook = subprocess.run([sys.executable, os.path.join(HERE, "ledger-stop.py")], capture_output=True, text=True,
                      input=json.dumps({"cwd": worktree, "transcript_path": transcript}),
                      env={**os.environ, "HOME": tmp})
blocked = json.loads(hook.stdout)
assert blocked["decision"] == "block" and "9.md" in blocked["reason"] and "6.md" not in blocked["reason"], hook.stdout


def stop_hook(command, cwd):
    event = {"timestamp": "2099-01-01T00:00:00Z", "message": {"content": [
        {"type": "tool_use", "name": "Bash", "input": {"command": command}}]}}
    open(transcript, "w").write(json.dumps(event) + "\n")
    out = subprocess.run([sys.executable, os.path.join(HERE, "ledger-stop.py")], capture_output=True, text=True,
                         input=json.dumps({"cwd": cwd, "transcript_path": transcript}), env={**os.environ, "HOME": tmp})
    return json.loads(out.stdout) if out.stdout.strip() else None


assert stop_hook('python3 ~/.agents/ship/dispatch.py --out x.out -- maestri ask "Jon 9" "$(cat p.md)"', worktree), "dispatch.py form"
assert stop_hook("git -C /x push origin feat/9", worktree), "git -C push"
assert stop_hook("cd /x && git push", worktree), "git push after &&"
assert stop_hook('cat <<E\nmaestri ask "Jon 9" "x"\nE', worktree) is None, "heredoc text"
assert stop_hook('maestri ask "Jon 9" "go"', os.path.join(ground, ".maestri", "roles", "0a1b")) is None, "a seat is never blocked"
assert stop_hook('maestri ask "Jon 9" "go"', os.path.join(worktree, ".maestri", "roles", "0a1b")), "a floor Maestro in a role folder is"
# Reminders: a head field. A "tell Lucas" log line with no Reminders field blocks the turn, once the field is there it passes.
assert ledger.read(write("R-1.md", head("R-1").replace("Next: do x", "Next: do x\nReminders: UAT first")))[0]["reminders"] == "UAT first"
remind = write("R-2.md", head("R-2") + "- 10:05 tell Lucas later about the waived case\n")
out = stop_hook("ls", worktree)
assert out and "Reminders" in out["reason"] and "R-2.md" in out["reason"], out
write("R-2.md", head("R-2").replace("Next: do x", "Next: do x\nReminders: waived case") + "- 10:05 tell Lucas later about the waived case\n")
assert stop_hook("ls", worktree) is None, "Reminders field present"
os.remove(remind)

# Thread: a color, or none.
assert ledger.read(write("T-1.md", head("T-1").replace("Maestro: m", "Maestro: m\nThread: Pink")))[0]["thread"] == "pink"
assert ledger.read(write("T-2.md", head("T-2").replace("Maestro: m", "Maestro: m\nThread: none")))[0]["thread"] == ""
assert ledger.read(write("T-3.md", head("T-3")))[0]["thread"] == ""

print("ok")
