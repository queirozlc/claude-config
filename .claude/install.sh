#!/usr/bin/env sh
# Installs the external tools this ~/.claude config depends on. Idempotent.
# Usage: sh ~/.claude/install.sh
set -u

have() { command -v "$1" >/dev/null 2>&1; }
say() { printf '\n==> %s\n' "$*"; }
os=$(uname -s)
arch=$(uname -m)

say "Prerequisites"
for bin in git jq node npm claude; do
  have "$bin" && printf '  ok   %s\n' "$bin" || printf '  MISSING %s\n' "$bin"
done
if ! have jq; then
  case "$os" in
    Darwin) have brew && brew install jq ;;
    Linux)  have apt-get && sudo apt-get install -y jq ;;
  esac
fi
if ! have node || ! have claude; then
  echo "Install node (https://nodejs.org) and Claude Code (npm i -g @anthropic-ai/claude-code), then re-run."
  exit 1
fi

say "codegraph  https://github.com/colbymchenry/codegraph"
have codegraph || npm i -g @colbymchenry/codegraph
codegraph install   # wires MCP server + prompt hook into Claude Code

say "ai-memory  https://github.com/akitaonrails/ai-memory"
if ! have ai-memory; then
  case "$os" in
    Darwin)
      case "$arch" in arm64) tgz=ai-memory-macos-aarch64.tar.gz ;; *) tgz=ai-memory-macos-x86_64.tar.gz ;; esac
      dir=$HOME/Applications/ai-memory
      mkdir -p "$dir" "$HOME/.local/bin" "$HOME/Library/Logs/ai-memory"
      curl -fsSL -o "$dir/$tgz" "https://github.com/akitaonrails/ai-memory/releases/latest/download/$tgz"
      tar -xzf "$dir/$tgz" -C "$dir"
      ln -sfn "$dir/ai-memory" "$HOME/.local/bin/ai-memory"
      "$dir/ai-memory" init
      plist=$dir/packaging/launchd/com.github.akitaonrails.ai-memory.plist
      if [ -f "$plist" ]; then
        sed -e "s|__AI_MEMORY_BIN__|$dir/ai-memory|" -e "s|__HOME__|$HOME|" "$plist" \
          > "$HOME/Library/LaunchAgents/com.github.akitaonrails.ai-memory.plist"
        launchctl bootstrap "gui/$(id -u)" "$HOME/Library/LaunchAgents/com.github.akitaonrails.ai-memory.plist"
      fi
      ;;
    *)
      echo "  Linux: see https://github.com/akitaonrails/ai-memory#installation (AUR: yay -S ai-memory-bin, or Docker)."
      echo "  Then re-run this script to wire hooks."
      ;;
  esac
fi
if have ai-memory; then
  export PATH="$HOME/.local/bin:$PATH"
  ai-memory install-hooks --agent claude-code --apply   # rewrites hook paths in settings.json for this machine
  ai-memory install-mcp   --client claude-code --apply
fi

say "Maestri CLI (ships inside the Maestri desktop app)"
maestri_cli=/Applications/Maestri.app/Contents/Resources/maestri
if [ -x "$maestri_cli" ]; then
  case "$(basename "${SHELL:-zsh}")" in bash) rc=$HOME/.bashrc ;; *) rc=$HOME/.zshrc ;; esac
  if grep -q MAESTRI_CLI "$rc" 2>/dev/null; then
    echo "  already in $rc"
  else
    printf '\n# Maestri CLI\nexport MAESTRI_CLI="%s"\nexport PATH="$(dirname "$MAESTRI_CLI"):$PATH"\n' "$maestri_cli" >> "$rc"
    echo "  added to $rc. Open a new shell to pick it up."
  fi
else
  echo "  Maestri.app not found in /Applications. Install the Maestri app, then re-run this script."
fi

say "Claude Code plugins"
claude plugin marketplace add DietrichGebert/ponytail      >/dev/null 2>&1 || true   # ponytail
claude plugin marketplace add paper-design/agent-plugins   >/dev/null 2>&1 || true   # paper
for p in ponytail@ponytail paper-desktop@paper atlassian@claude-plugins-official typescript-lsp@claude-plugins-official; do
  claude plugin install -y "$p" || true
done

say "MCP servers (user scope, stored in ~/.claude.json)"
claude mcp add -s user --transport http context7 https://mcp.context7.com/mcp 2>/dev/null || true
claude mcp add -s user --transport http mobbin   https://api.mobbin.com/mcp   2>/dev/null || true

say "Done. Dangling skill symlinks (expected: elixir, a local project link):"
find "$HOME/.claude/skills" -maxdepth 1 -type l ! -exec test -e {} \; -print
