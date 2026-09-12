# mise shims for non-interactive shells. ~/.zshrc runs `mise activate` but is
# only sourced for interactive shells, so scripts spawned from launchd, cron,
# git hooks, or GUI apps fell back to /usr/bin/ruby (system 2.6). Shims resolve
# the per-directory version without needing activation.
# ~/.local/bin (uv, and friends) has the same problem: it is only exported from
# ~/.zshrc, so bin/ci's Python steps vanish in a non-interactive shell.
export PATH="$HOME/.local/share/mise/shims:$HOME/.local/bin:$PATH"

# Company-specific GitHub configuration for terminals and agent shells.
source /Users/lucasqueiroz/.config/github/shell.zsh
