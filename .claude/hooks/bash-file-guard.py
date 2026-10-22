#!/usr/bin/env python3
"""Claude Code Bash hook: keep edits of project files on Read/Edit/Write.

PreToolUse: deny a Bash command that writes a path inside the session cwd
(redirects, tee, sed/perl -i, inline python/node/ruby/bash write calls).
Writes outside the cwd, such as /tmp scripts, stay allowed.

PostToolUse: if project files changed anyway (a /tmp script that edits the
repo, a path in a variable), tell Claude through additionalContext. The hook
cannot undo the change.

Self-check: python3 ~/.claude/hooks/bash-file-guard.py --test
"""
import ast
import contextlib
import glob
import io
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile

SPLIT_CHARS = set(";|&()\n")
OPERATOR_CHARS = set("<>&|")
REDIRECTS = {">", ">>", ">|", "&>", "&>>"}
WRAPPERS = {"sudo", "env", "time", "nohup", "command", "exec", "xargs", "nice"}
INPLACE_TOOLS = {"sed", "gsed", "perl"}
CODE_FLAGS = {
    "python": {"-c"},
    "node": {"-e", "--eval", "-p", "--print"},
    "bun": {"-e", "--eval"},
    "ruby": {"-e"},
    "bash": {"-c"},
    "sh": {"-c"},
    "zsh": {"-c"},
}
# Programs whose file changes in the project are expected: git, packages,
# generators, formatters, plain file moves, and read-only filters.
ALLOWED_WRITERS = {
    "git", "gh", "cd", "ls", "cat", "echo", "printf", "head", "tail", "grep",
    "rg", "sort", "uniq", "wc", "jq", "cut", "tr", "true", "test", "find",
    "mkdir", "rm", "rmdir", "mv", "cp", "ln", "touch", "chmod", "tar", "unzip",
    "curl", "wget", "npm", "npx", "pnpm", "yarn", "bun", "bunx", "bundle",
    "rake", "rails", "rspec", "mix", "go", "gofmt", "cargo", "make", "just",
    "uv", "pip", "pip3", "poetry", "ruff", "black", "isort", "prettier",
    "eslint", "biome", "rubocop", "standardrb", "terraform", "docker",
    "codegraph",
}
HEREDOC = re.compile(r"(?<!<)<<(-?)[ \t]*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\2")
PLACEHOLDER = re.compile(r"__HEREDOC_(\d+)__")
JS_RB_WRITE = re.compile(
    r"""(?:writeFileSync|appendFileSync|writeFile|appendFile|File\.write|IO\.write)"""
    r"""\s*\(\s*(['"])([^'"]+)\1"""
)


def split_heredocs(cmd):
    """Replace each heredoc with a placeholder token. Return the text and the bodies."""
    lines, out, bodies, i = cmd.split("\n"), [], [], 0
    while i < len(lines):
        found = []

        def mark(match):
            found.append((match.group(1), match.group(3)))
            bodies.append("")
            return "<< __HEREDOC_%d__" % (len(bodies) - 1)

        out.append(HEREDOC.sub(mark, lines[i]))
        i += 1
        for n, (dash, delim) in enumerate(found, start=len(bodies) - len(found)):
            body = []
            while i < len(lines) and (lines[i].lstrip("\t") if dash else lines[i]) != delim:
                body.append(lines[i])
                i += 1
            i += 1
            bodies[n] = "\n".join(body)
    return "\n".join(out), bodies


def tokenize(text):
    lex = shlex.shlex(text.replace("\\\n", " "), posix=True, punctuation_chars="();<>|&\n")
    lex.whitespace = " \t\r"
    lex.whitespace_split = True
    lex.commenters = ""
    return list(lex)


def is_operator(tok, chars):
    return bool(tok) and set(tok) <= chars


def segments(tokens):
    seg = []
    for tok in tokens:
        if is_operator(tok, SPLIT_CHARS):
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def args_after(seg, i):
    out = []
    for tok in seg[i + 1:]:
        if is_operator(tok, OPERATOR_CHARS):
            break
        out.append(tok)
    return out


def inside(path, base, root, must_exist=False):
    p = os.path.expandvars(os.path.expanduser(path))
    if not base or not p or "$" in p:
        return False
    full = os.path.join(base, p)
    matches = glob.glob(full) if any(c in p for c in "*?[") else [full]
    for match in matches:
        if must_exist and not os.path.exists(match):
            continue
        real = os.path.realpath(match)
        if real == root or real.startswith(root + os.sep):
            return True
    return False


def interp_kind(tok):
    name = os.path.basename(tok)
    if re.fullmatch(r"python[0-9.]*", name):
        return "python"
    return name if name in CODE_FLAGS else None


def inline_code(kind, rest, bodies):
    """The code an interpreter runs from its flag, heredoc or here-string. "" for a script file."""
    for j, arg in enumerate(rest):
        if is_operator(arg, OPERATOR_CHARS):
            break
        if arg in CODE_FLAGS[kind]:
            return rest[j + 1] if j + 1 < len(rest) else ""
        if arg != "-" and not arg.startswith("-"):
            return ""
    for j, arg in enumerate(rest[:-1]):
        placeholder = PLACEHOLDER.fullmatch(rest[j + 1])
        if arg == "<<" and placeholder:
            return bodies[int(placeholder.group(1))]
        if arg == "<<<":
            return rest[j + 1]
    return ""


def keyword(node, arg):
    return next((k.value for k in node.keywords if k.arg == arg), None)


def is_write_mode(node):
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and bool(set(node.value) & set("wax+"))
    )


def literal_path(node):
    """The path a literal expression names: "a", Path("a"), Path("a") / "b"."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Call) and node.args:
        return literal_path(node.args[0])
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left, right = literal_path(node.left), literal_path(node.right)
        return os.path.join(left, right) if left and right else None
    return None


def py_write_targets(code):
    """Literal paths that Python code opens for writing. Computed paths are left to PostToolUse."""
    try:
        tree = ast.parse(code)
    except (SyntaxError, ValueError):
        return []
    targets = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func, args = node.func, node.args
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
        owner = func.value if isinstance(func, ast.Attribute) else None
        owner_name = getattr(owner, "id", "")
        if name == "open" and owner is None:
            if args and is_write_mode(args[1] if len(args) > 1 else keyword(node, "mode")):
                targets.append(args[0])
        elif name == "open" and isinstance(owner, (ast.Call, ast.BinOp)):
            if is_write_mode(args[0] if args else keyword(node, "mode")):
                targets.append(owner)
        elif name in ("write_text", "write_bytes") and owner is not None:
            targets.append(owner)
        elif name in ("copy", "copy2", "copyfile", "copytree", "move") and owner_name == "shutil" and len(args) > 1:
            targets.append(args[1])
        elif name in ("replace", "rename") and owner_name == "os" and len(args) > 1:
            targets.append(args[1])
    return [p for p in map(literal_path, targets) if p]


def violations(cmd, root, base=None):
    """(what, path) pairs for the writes this command makes inside root.

    base is the directory relative paths resolve against; "" means unknown
    (after `cd "$DIR"`), which skips the path checks and leaves them to PostToolUse.
    """
    base = root if base is None else base
    text, bodies = split_heredocs(cmd)
    try:
        tokens = tokenize(text)
    except ValueError:
        return []
    found = []
    for seg in segments(tokens):
        if seg[0] == "cd":
            target = os.path.expandvars(os.path.expanduser(seg[1] if len(seg) > 1 else "~"))
            known = "$" not in target and target != "-" and (base or os.path.isabs(target))
            base = os.path.join(base, target) if known else ""
            continue
        for i, tok in enumerate(seg):
            name = os.path.basename(tok)
            args = args_after(seg, i)
            kind = interp_kind(tok)
            if tok in REDIRECTS and i + 1 < len(seg) and inside(seg[i + 1], base, root):
                found.append(("a shell redirect", seg[i + 1]))
            elif name == "tee":
                found += [("tee", a) for a in args if not a.startswith("-") and inside(a, base, root)]
            elif name in INPLACE_TOOLS and any(re.match(r"-(-in-place|[A-Za-z0-9]*i)", a) for a in args):
                found += [
                    (name + " -i", a)
                    for a in args
                    if not a.startswith("-") and inside(a, base, root, must_exist=True)
                ]
            elif kind:
                code = inline_code(kind, seg[i + 1:], bodies)
                if kind in ("bash", "sh", "zsh"):
                    found += violations(code, root, base) if code else []
                    continue
                paths = py_write_targets(code) if kind == "python" else [m.group(2) for m in JS_RB_WRITE.finditer(code)]
                found += [(kind + " code", p) for p in paths if inside(p, base, root)]
    return found


def programs(cmd):
    """First program of each simple command. A redirect to a computed path counts as unknown."""
    text, _ = split_heredocs(cmd)
    try:
        tokens = tokenize(text)
    except ValueError:
        return {"<unparsed>"}
    names = set()
    for seg in segments(tokens):
        for i, tok in enumerate(seg):
            if tok in REDIRECTS and i + 1 < len(seg) and "$" in seg[i + 1]:
                names.add("<redirect>")
        for tok in seg:
            name = os.path.basename(tok)
            if re.match(r"[A-Za-z_]\w*=", tok) or name in WRAPPERS or tok.startswith("-"):
                continue
            names.add(name)
            break
    return names


def git_state(cwd):
    """{path: [mtime_ns, size] or None} for the changed and untracked paths under cwd."""
    def git(*args):
        return subprocess.run(
            ["git", "-C", cwd] + list(args), capture_output=True, text=True, timeout=5, check=True
        ).stdout

    top = git("rev-parse", "--show-toplevel").strip()
    entries = iter(git("status", "--porcelain=v1", "-z", "--untracked-files=all", "--", ".").split("\0"))
    state = {}
    for entry in entries:
        if len(entry) < 4:
            continue
        if entry[0] in "RC":
            next(entries, None)
        try:
            st = os.stat(os.path.join(top, entry[3:]))
            state[entry[3:]] = [st.st_mtime_ns, st.st_size]
        except OSError:
            state[entry[3:]] = None
    return state


def snapshot_file(payload):
    name = re.sub(r"[^\w-]", "", payload.get("tool_use_id") or "") or "none"
    return os.path.join(tempfile.gettempdir(), "claude-bash-file-guard", name + ".json")


def emit(event, **fields):
    print(json.dumps({"hookSpecificOutput": dict(hookEventName=event, **fields)}))


def pre(payload, cmd, root):
    found = violations(cmd, root)
    if found:
        what, path = found[0]
        emit(
            "PreToolUse",
            permissionDecision="deny",
            permissionDecisionReason=(
                "bash-file-guard: %s writes %s, which is inside the project (%s). "
                "Use the Read, Edit and Write tools for project files. "
                "If this is a data transform, print the result to stdout or write it to the "
                "scratchpad or /tmp, then run the command again. "
                "Bash and scripts that write outside the project are allowed."
                % (what, path, root)
            ),
        )
        return
    try:
        state = git_state(root)
    except (OSError, subprocess.SubprocessError):
        return
    path = snapshot_file(payload)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(state, f)


def post(payload, cmd, root):
    path = snapshot_file(payload)
    try:
        with open(path) as f:
            before = json.load(f)
        os.remove(path)
        after = git_state(root)
    except (OSError, ValueError, subprocess.SubprocessError):
        return
    changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
    if not changed or programs(cmd) <= ALLOWED_WRITERS:
        return
    emit(
        "PostToolUse",
        additionalContext=(
            "bash-file-guard: project files changed during this Bash call: %s. "
            "If this command changed them, use the Read, Edit and Write tools for project files, "
            "or tell the user why Bash was necessary. Changes from other tools that ran at the "
            "same time can also appear here." % ", ".join(changed[:10])
        ),
    )


def project_root(cwd):
    """The git work tree that holds cwd. Maestri seats start in <repo>/.maestri/roles/<id>."""
    try:
        top = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, timeout=5, check=True,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return cwd
    return os.path.realpath(top) if top else cwd


def main():
    payload = json.load(sys.stdin)
    if payload.get("tool_name") != "Bash":
        return
    root = project_root(os.path.realpath(payload.get("cwd") or os.getcwd()))
    if root == os.path.realpath(os.path.expanduser("~")):
        return
    cmd = (payload.get("tool_input") or {}).get("command") or ""
    event = payload.get("hook_event_name")
    if event == "PreToolUse":
        pre(payload, cmd, root)
    elif event == "PostToolUse":
        post(payload, cmd, root)


def test():
    root = os.path.realpath(tempfile.mkdtemp())
    os.makedirs(os.path.join(root, "lib"))
    open(os.path.join(root, "lib", "x.rb"), "w").close()
    deny = [
        "cat > src/app.rb <<EOF\nputs 1\nEOF",
        "sed -i '' 's/a/b/' lib/x.rb",
        "perl -pi -e 's/a/b/' lib/*.rb",
        "echo hi | tee -a notes.md",
        "python3 - <<'PY'\nopen('config/x.yml', 'w').write('a')\nPY",
        "python3 -c \"import pathlib; pathlib.Path('lib/x.rb').write_text('y')\"",
        "node -e \"require('fs').writeFileSync('a.json', '{}')\"",
        "bash -c \"sed -i s/a/b/ lib/x.rb\"",
        "npm test > test.log 2>&1",
    ]
    allow = [
        "git commit -m \"$(cat <<'EOF'\nfix: a > b, it's done\nEOF\n)\"",
        "cat > /tmp/notes.md <<EOF\nx\nEOF",
        "sed -n '1,5p' lib/x.rb",
        "python3 -c 'import json; print(json.dumps({}))'",
        "python3 - <<'PY'\nprint(open('lib/x.rb').read())\nopen('/tmp/out.txt', 'w').write('x')\nPY",
        "python3 /tmp/gen.py",
        "ls -la 2>/dev/null",
        "cd /tmp && python3 -c \"open('x.txt', 'w')\"",
        "D=$(mktemp -d) && cd \"$D\" && echo a > lib/x.rb",
        "echo \"a > b\" && grep -rn \"x\" lib | head -5",
    ]
    for cmd in deny:
        assert violations(cmd, root), "should deny: " + cmd
    for cmd in allow:
        assert not violations(cmd, root), "should allow: %s -> %s" % (cmd, violations(cmd, root))

    subprocess.run(["git", "init", "-q", root], check=True)
    seat = os.path.join(root, ".maestri", "roles", "seat")
    os.makedirs(seat)
    assert project_root(seat) == root, "a seat dir should resolve to its repo"
    assert violations("sed -i '' s/a/b/ ../../../lib/x.rb", project_root(seat), seat), "should deny from a seat dir"

    def round_trip(cmd, change):
        payload = {"tool_use_id": "toolu_test", "tool_input": {"command": cmd}}
        pre(payload, cmd, root)
        with open(os.path.join(root, "lib", "x.rb"), "a") as f:
            f.write(change)
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            post(payload, cmd, root)
        return out.getvalue()

    assert "lib/x.rb" in round_trip("python3 /tmp/fix.py", "a"), "should report a /tmp script edit"
    assert round_trip("npm install", "b") == "", "should not report an allowed program"
    assert "lib/x.rb" in round_trip('echo x > "$F"', "c"), "should report a redirect to a variable"
    print("ok")


if __name__ == "__main__":
    if sys.argv[1:] == ["--test"]:
        test()
        sys.exit()
    try:
        main()
    except Exception:
        # ponytail: fail open. A bug in this steering hook must not block every Bash call.
        pass
