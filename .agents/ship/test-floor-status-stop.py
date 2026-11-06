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


def run(events, env=True, active=False, maestri=None, cwd="/tmp/ground", home=None):
    transcript = os.path.join(tmp, "t.jsonl")
    open(transcript, "w").write("\n".join(json.dumps(e) for e in events))
    e = {k: v for k, v in os.environ.items() if not k.startswith("MAESTRI")}
    if home:
        e["HOME"] = home
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
assert run([user("go"), tool("Bash", command="pnpm cdk deploy App")], maestri=same, cwd=floor_dir) is not None, "deploy is work"
dispatch = tool("Bash", command='python3 ~/.agents/ship/dispatch.py --out x.out -- maestri ask "Gon" "$(cat p.md)"')
assert run([user("go"), dispatch], maestri=same, cwd=floor_dir) is not None, "dispatch.py ask is work"
assert run([user("go"), tool("Bash", command="git -C /x push origin y")], maestri=same, cwd=floor_dir) is not None, "git -C push is work"
state_first = tool("Bash", command='maestri floor status --state review "Jon: PR ready"')
assert run([user("go"), EDIT, result(), state_first, result()], maestri=same, cwd=floor_dir) is None, "--state before the text"
cli_var = tool("Bash", command='"$MAESTRI_CLI" floor status "Jon: x" --progress 2/5')
assert run([user("go"), EDIT, result(), cli_var, result()], maestri=same, cwd=floor_dir) is None, "$MAESTRI_CLI form"
heredoc_status = tool("Bash", command='cat <<E\nmaestri floor status "fake"\nE')
assert run([user("go"), EDIT, result(), heredoc_status, result()], maestri=same, cwd=floor_dir) is not None, "status in a heredoc is text"

# Ground level: the ground Maestro wrote a floor ledger this turn.
home = os.path.join(tmp, "home")
repo = os.path.join(home, "proj")
os.makedirs(repo)
subprocess.run(["git", "init", "-q", repo], check=True)
state = os.path.join(home, ".agents/ship/state/proj")
os.makedirs(state)
def ledger_file(key, floor, phase="6-pr-open", extra=""):
    open(os.path.join(state, f"{key}.md"), "w").write(f"Master: Ned\n--\n# {key} — cycle state\n\nPhase: {phase}\nFloor: {floor}\n{extra}\n## Log\n")
ledger_file("LOC-1", "LOC-1 login · /x/.maestri/floors/proj--loc-1")
ledger_file("LOC-2", "Ground")
ground_cli = cli(0, "Ned: floors ok", "Ned: floors ok")
APPEND = tool("Bash", command='echo "- 13:00 deployed" >> $S/LOC-1.md')
FLOOR_POSTED = tool("Bash", command='maestri floor status --floor "LOC-1 login" "Ned: deployed" --state review')
def ground_run(*events):
    return run([{**user("go"), "timestamp": "2000-01-01T00:00:00Z"}, *events], maestri=ground_cli, cwd=repo, home=home)
wrote = ground_run(APPEND, result())
assert wrote and "LOC-1 login: Ned: floors ok" in wrote["reason"] and "--floor" in wrote["reason"], wrote
assert ground_run(APPEND, result(), FLOOR_POSTED, result()) is None, "floor posted with --floor"
assert ground_run(tool("Bash", command='echo x >> $S/LOC-2.md')) is None, "ground cycle ledger"
assert ground_run(tool("Bash", command="cat $S/LOC-1-brief.md")) is None, "sibling file is not the ledger"
old = run([{**user("go"), "timestamp": "2999-01-01T00:00:00Z"}, APPEND], maestri=ground_cli, cwd=repo, home=home)
assert old is None, "ledger not changed since the turn started: a read"
# Another agent writes the ledger while this turn only reads it.
for read in ["sed -n '1,20p' $S/LOC-1.md", "tail -40 $S/LOC-1.md", "grep -n Lucas $S/LOC-1.md | head", "wc -c < $S/LOC-1.md"]:
    assert ground_run(tool("Bash", command=read), result()) is None, f"a read is not a write: {read}"
assert ground_run(tool("Edit", file_path=f"{state}/LOC-1.md"), result()) is not None, "Edit tool on the ledger is a write"
assert ground_run(tool("Bash", command=f"tee -a {state}/LOC-1.md <<E\n- 13:00 x\nE"), result()) is not None, "tee is a write"
flags_first = tool("Bash", command='maestri floor status --floor "LOC-1 login" --state review "Ned: deployed"')
assert ground_run(APPEND, result(), flags_first, result()) is None, "--state before the text, with --floor"
text_first = tool("Bash", command='maestri floor status "Ned: deployed" --floor "LOC-1 login"')
assert ground_run(APPEND, result(), text_first, result()) is None, "text before --floor"
ledger_file("LOC-1", "LOC-1 login · /x/.maestri/floors/proj--loc-1", extra="Routed from: other\n")
assert ground_run(APPEND) is None, "routed ledger: the floor is in another workspace"
ledger_file("LOC-1", "LOC-1 login · /x/.maestri/floors/proj--loc-1")
unreachable = os.path.join(tmp, "maestri-unreachable")
open(unreachable, "w").write("#!/bin/sh\ncase \"$*\" in *LOC-1*) echo 'No floor named \"LOC-1 login\" in this workspace' >&2; exit 1;; *) echo 'Ned: floors ok';; esac\n")
os.chmod(unreachable, os.stat(unreachable).st_mode | stat.S_IXUSR)
assert run([{**user("go"), "timestamp": "2000-01-01T00:00:00Z"}, APPEND], maestri=unreachable, cwd=repo, home=home) is None, "floor status cannot reach the floor"
ledger_file("LOC-1", "LOC-1 login · /x/.maestri/floors/proj--loc-1", phase="paused (6-pr-open)")
assert ground_run(APPEND) is None, "paused ledger"
print("ok")
