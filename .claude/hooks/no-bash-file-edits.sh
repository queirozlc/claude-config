#!/usr/bin/env bash
# PreToolUse hook for Bash: block file edits done through the shell.
# Files are changed with the Read/Edit/Write tools only (global CLAUDE.md).
cmd=$(jq -r '.tool_input.command // ""')

if printf '%s' "$cmd" | grep -qE \
  -e '(^|[;&| ])(sed|perl) +-[a-zA-Z]*i' \
  -e '(^|[;&| ])python[0-9.]* +(-c|-|- +)' \
  -e '<<' \
  -e '(^|[;&| ])tee( |$)' \
  -e '(^|[^0-9&>=-])>>? *[^&/> ]' \
  -e '(^|[^0-9&>=-])>>? */(tmp|Users|home|private)'; then
  echo "Blocked: this command edits or writes a file from Bash. Use the Read, Edit or Write tool instead." >&2
  exit 2
fi
exit 0
