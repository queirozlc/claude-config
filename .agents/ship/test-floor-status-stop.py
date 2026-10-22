#!/usr/bin/env python3
"""Runnable check for floor-status-stop.py: python3 test-floor-status-stop.py"""
import json, os, stat, subprocess, sys, tempfile

HOOK = os.path.join(os.path.dirname(os.path.abspath(__file__)), "floor-status-stop.py")
tmp = tempfile.mkdtemp()


def cli(exit_code, text, ground='"Ground" has no status yet.'):
    """A fake maestri: `floor status --floor Ground` prints `ground`, plain `floor status` prints `text`."""
    path = os.path.join(tmp, f"maestri{abs(hash((exit_code, text, ground)))}")
    open(path, "w").write(f"#!/bin/sh\ncase \"$*\" in *Ground*) echo '{ground}';; *) echo '{text}';; esac\nexit {exit_code}\n")
    os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR)
    return path


def user(text):
    return {"type": "user", "message": {"role": "user", "content": text}}


def result():
    return {"type": "user", "message": {"role": "user", "content": [{"type": "tool_result", "content": "ok"}]}}


def tool(name, **input):
    return {"type": "assistant", "message": {"role": "assistant", "content": [{"type": "tool_use", "name": name, "input": input}]}}


def run(events, env=True, active=False, maestri=None, cwd="/tmp/ground"):
    transcript = os.path.join(tmp, "t.jsonl")
    open(transcript, "w").write("\n".join(json.dumps(e) for e in events))
    e = {k: v for k, v in os.environ.items() if not k.startswith("MAESTRI")}
    if env:
        e["MAESTRI_TERMINAL_ID"] = "t"
        e["MAESTRI_CLI"] = maestri or cli(0, "Jon: gate green")
    out = subprocess.run(["python3", HOOK], input=json.dumps({"transcript_path": transcript, "stop_hook_active": active, "cwd": cwd}),
                         capture_output=True, text=True, env=e)
    return json.loads(out.stdout) if out.stdout.strip() else None


POST = tool("Bash", command='maestri floor status "Jon: gate green" --progress 3/4')
EDIT = tool("Edit", file_path="a.ts")

blocked = run([user("go"), EDIT, result()])
assert blocked and blocked["decision"] == "block" and "Jon: gate green" in blocked["reason"], blocked
assert run([user("go"), EDIT, result(), POST, result()]) is None, "posted this turn"
assert run([user("go"), tool("Bash", command="maestri say 'hi'")]) is None, "chat only"
assert run([user("go"), EDIT, result(), user("next")]) is None, "new prompt resets the turn"
assert run([user("go"), tool("Bash", command="cd x && git commit -m y")]) is not None, "cycle event is work"
assert run([user("go"), tool("Bash", command='cat <<E\nmaestri ask "A" "x"\nE')]) is None, "heredoc text is not work"
assert run([user("go"), EDIT], active=True) is None, "stop_hook_active"
assert run([user("go"), EDIT], env=False) is None, "not in Maestri"
assert run([user("go"), EDIT], maestri=cli(1, "no floor")) is None, "maestri cannot answer"
ground = '"Ground" has no status yet.'
assert run([user("go"), EDIT], maestri=cli(0, ground, ground)) is None, "ground level, empty status"
assert run([user("go"), EDIT], maestri=cli(0, "Maestro: floors ok", "Maestro: floors ok")) is None, "ground level, with status"
floor_dir = "/Users/me/Development/ravn/.maestri/floors/enerflo-next--en-4865-api-migration"
same = cli(0, ground, ground)
assert run([user("go"), EDIT], maestri=same, cwd=floor_dir) is not None, "floor by path, even with Ground's text"
assert run([user("go"), EDIT], maestri=same, cwd=floor_dir + "/.maestri/roles/jon") is None, "seat on a floor stays quiet"
maestro_role = os.path.join(tmp, ".maestri/floors/x--y/.maestri/roles/m")
os.makedirs(maestro_role)
open(os.path.join(maestro_role, "role.json"), "w").write('{"name": "LocalPay Floor Maestro"}')
assert run([user("go"), EDIT], maestri=same, cwd=maestro_role) is not None, "floor Maestro with a role"
assert run([user("go"), EDIT], maestri=same, cwd="/Users/me/Development/ravn/enerflo-next") is None, "ground checkout"
real = run([user("go"), EDIT], maestri=cli(0, '"hook-probe": [working] Probe: hook test  ·  by Probe', ground), cwd=floor_dir)
assert real and 'maestri floor status "Probe: hook test"' in real["reason"] and "by Probe" not in real["reason"], real
review = run([user("go"), EDIT], maestri=cli(0, '"EN-1": [review 83%] Morel: PR ready  ·  by Morel', ground), cwd=floor_dir)
assert review and 'maestri floor status "Morel: PR ready" --state review --progress 83%' in review["reason"], review
empty = run([user("go"), EDIT], maestri=cli(0, '"HOB-9" has no status yet.', ground))
assert empty and "(empty)" in empty["reason"], "floor with no status yet"
print("ok")
