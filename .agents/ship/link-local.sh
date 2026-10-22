#!/bin/zsh
# Sets up a checkout for the ship cycle: the ledger Stop hook, plus the
# CLAUDE.local.md link to the project house rules.
#   link-local.sh [dir]               hook + link one checkout (default: current dir)
#   link-local.sh --hook-only [dir]   hook only, no CLAUDE.local.md
#   link-local.sh --add <args>        git worktree add <args>, then hook + link the new worktree
set -eu

SHIP="$HOME/.agents/ship"
HOOK_ONLY=false

link() {
  local top main target rules
  top=$(git -C "$1" rev-parse --show-toplevel)
  main=$(git -C "$top" worktree list --porcelain | sed -n '1s/^worktree //p')

  # An existing link wins, then the main checkout's; either can point to another project's rules.
  if [[ -L "$top/CLAUDE.local.md" ]]; then
    target=$(readlink "$top/CLAUDE.local.md")
  elif [[ -L "$main/CLAUDE.local.md" ]]; then
    target=$(readlink "$main/CLAUDE.local.md")
  elif [[ -f "$top/.agents/CLAUDE.md" ]]; then
    target=.agents/CLAUDE.md
  elif [[ -f "$SHIP/${main:t}/CLAUDE.md" ]]; then
    target="$SHIP/${main:t}/CLAUDE.md"
  else
    target="$SHIP/CLAUDE.md"
  fi

  [[ "$target" == /* ]] && rules=$target || rules="$top/$target"

  if [[ ! -f "$rules" && ! -f "$top/.agents/ship.md" && ! -f "$top/.claude/ship.md" && ! -f "$SHIP/${main:t}/ship.md" ]]; then
    echo "skip $top: no ship config"
    return 0
  fi
  add_stop_hook "$top"

  $HOOK_ONLY && return 0
  [[ -f "$rules" ]] || { echo "skip link $top: no ship rules at $target"; return 0; }

  if [[ -e "$top/CLAUDE.local.md" || -L "$top/CLAUDE.local.md" ]]; then
    echo "skip $top: CLAUDE.local.md already exists"
  else
    ln -s "$target" "$top/CLAUDE.local.md"
    echo "linked $top/CLAUDE.local.md -> $target"
  fi

  ignore "$top" CLAUDE.local.md
}

# info/exclude lives in the common git dir, so every worktree shares it.
ignore() {
  git -C "$1" check-ignore -q "$2" && return 0
  echo "$2" >> "$(git -C "$1" rev-parse --path-format=absolute --git-common-dir)/info/exclude"
  echo "ignored $2 in .git/info/exclude"
}

add_stop_hook() {
  local settings="$1/.claude/settings.local.json" script hook
  mkdir -p "$1/.claude"
  [[ -s "$settings" ]] || echo '{}' > "$settings"
  for script in ledger-stop.py floor-status-stop.py; do
    hook="python3 $SHIP/$script"
    if jq -e --arg c "$hook" '[.hooks.Stop[]?.hooks[]?.command] | index($c)' "$settings" >/dev/null; then
      echo "skip $settings: $script already there"
    else
      jq --arg c "$hook" '.hooks.Stop += [{hooks: [{type: "command", command: $c}]}]' "$settings" > "$settings.tmp"
      mv "$settings.tmp" "$settings"
      echo "added $script Stop hook to $settings"
    fi
  done
  hook="python3 $SHIP/thread-guard.py"
  for event in PreToolUse UserPromptSubmit; do
    if jq -e --arg c "$hook" --arg e "$event" '[.hooks[$e][]?.hooks[]?.command] | index($c)' "$settings" >/dev/null; then
      echo "skip $settings: thread-guard.py $event already there"
    else
      jq --arg c "$hook" --arg e "$event" \
        '.hooks[$e] += [if $e == "PreToolUse" then {matcher: "Bash"} else {} end + {hooks: [{type: "command", command: $c}]}]' \
        "$settings" > "$settings.tmp"
      mv "$settings.tmp" "$settings"
      echo "added thread-guard.py $event hook to $settings"
    fi
  done
  ignore "$1" .claude/settings.local.json
}

if [[ "${1:-}" == "--hook-only" ]]; then
  HOOK_ONLY=true
  link "${2:-.}"
elif [[ "${1:-}" == "--add" ]]; then
  shift
  before=$(git worktree list --porcelain | sed -n 's/^worktree //p')
  git worktree add "$@"
  git worktree list --porcelain | sed -n 's/^worktree //p' | while read -r wt; do
    print -r -- "$before" | grep -qxF -- "$wt" || link "$wt"
  done
else
  link "${1:-.}"
fi
