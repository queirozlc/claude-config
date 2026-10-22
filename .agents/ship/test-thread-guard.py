#!/usr/bin/env python3
"""Runnable check for thread-guard.py: python3 test-thread-guard.py"""
import importlib.util, os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location("guard", os.path.join(HERE, "thread-guard.py"))
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)

state = tempfile.mkdtemp()
owned = [{"key": "EN-1", "thread": "pink"}, {"key": "EN-2", "thread": "blue"}]

# Only a real `maestri say` command counts, also behind an env tag or a &&.
assert guard.SAY.search("maestri say 'hi'")
assert guard.SAY.search("SHIP_TICKET=EN-1 maestri say <<'EOF'")
assert guard.SAY.search("cd x && SHIP_TICKET=none maestri say --progress 'x'")
assert not guard.SAY.search("cat <<'EOF'\nuse maestri say to answer\nEOF")
assert not guard.SAY.search("maestri ask Gon 'x'")

# Tagged reply in its own thread, or tagged none: allowed.
assert guard.check_say("SHIP_TICKET=EN-1 maestri say x", state, owned, "pink") is None
assert guard.check_say("SHIP_TICKET=none maestri say x", state, owned, "pink") is None
# Tagged reply while the person is in another ticket's thread: denied, outbox named.
reason = guard.check_say("SHIP_TICKET=EN-1 maestri say x", state, owned, "blue")
assert reason and "EN-1-outbox.md" in reason and "pink" in reason
# Untagged reply in a ticket thread: denied. In a free thread: allowed.
assert "SHIP_TICKET=EN-2" in guard.check_say("maestri say x", state, owned, "blue")
assert guard.check_say("maestri say x", state, owned, "green") is None
# A key with no thread (or a closed ticket) is not guarded.
assert guard.check_say("SHIP_TICKET=EN-9 maestri say x", state, owned, "blue") is None

# A message from pink gets EN-1's waiting outbox and the thread map.
header = "---\nBelow is a message from the user through Maestri Chat.\nReply only via `maestri say`.\nthread: pink\n---\n\nhi"
open(os.path.join(state, "EN-1-outbox.md"), "w").write("## 10:00\nupdate\n")
context = guard.pending(header, state, owned)
assert "EN-1-outbox.md" in context and "EN-2 → blue" in context
assert guard.pending("no header here", state, owned) is None

print("ok")
