#!/usr/bin/env bash
input="$(cat)"

RESET=$'\033[0m'
DIM=$'\033[2;90m'
MAGENTA=$'\033[1;35m'
YELLOW=$'\033[1;33m'
GREEN=$'\033[32m'
RED=$'\033[31m'

model=$(jq -r '.model.display_name // "?"' <<<"$input")
user=$(whoami)

used=$(jq -r '[.context_window.used_percentage, .context.used_percent, .context_window.used_percent] | map(select(. != null)) | first // empty' <<<"$input")
if [ -n "$used" ]; then
  ctx_pct=$(printf '%.0f' "$used")
else
  ctx_pct="?"
fi

ctx_size=$(jq -r '.context_window.context_window_size // 0' <<<"$input")
tok_used=$(jq -r '[.context_window.total_input_tokens, .context.total_input_tokens, .usage.input_tokens] | map(select(. != null)) | first // 0' <<<"$input")
fmt_tokens() { # $1=tokens -> "12.3k" / "1.2M"
  local n="$1"
  if [ "$n" -ge 1000000 ] 2>/dev/null; then
    printf '%.1fM' "$(echo "$n" | awk '{printf "%f", $1/1000000}')"
  elif [ "$n" -ge 1000 ] 2>/dev/null; then
    printf '%.1fk' "$(echo "$n" | awk '{printf "%f", $1/1000}')"
  else
    printf '%s' "$n"
  fi
}
bar=""
if [ "$ctx_pct" != "?" ]; then
  bar_width=10
  filled=$(( ctx_pct * bar_width / 100 ))
  [ "$filled" -gt "$bar_width" ] && filled="$bar_width"
  bar_color="$GREEN"
  [ "$ctx_pct" -ge 50 ] && bar_color="$YELLOW"
  [ "$ctx_pct" -ge 80 ] && bar_color="$RED"
  bar="["
  for ((i=0; i<bar_width; i++)); do
    if [ "$i" -lt "$filled" ]; then bar="${bar}█"; else bar="${bar}░"; fi
  done
  bar="${bar}]"
  tok_str="$(fmt_tokens "$tok_used")"
  [ "$ctx_size" -gt 0 ] 2>/dev/null && tok_str="${tok_str}/$(fmt_tokens "$ctx_size")"
  bar="${bar_color}${bar}${RESET} ${DIM}${tok_str}${RESET}"
fi

cache_read=$(jq -r '[.context_window.current_usage.cache_read_input_tokens, .context.cache_read_input_tokens, .usage.cache_read_input_tokens] | map(select(. != null)) | first // 0' <<<"$input")
total_input=$(jq -r '[.context_window.total_input_tokens, .context.total_input_tokens, .usage.input_tokens] | map(select(. != null)) | first // 0' <<<"$input")
if [ "${total_input:-0}" -gt 0 ] 2>/dev/null; then
  cache_pct=$(( (cache_read * 100) / total_input ))
else
  cache_pct=0
fi
cache_warn=""
cache_color="$GREEN"
if [ "$cache_pct" -lt 20 ]; then
  cache_warn=" ⚠"
  cache_color="$RED"
fi

effort=$(jq -r '.effort.level // empty' <<<"$input")
[ -z "$effort" ] && effort="${CLAUDE_REASONING_EFFORT:-}"

cwd=$(jq -r '.workspace.current_dir // .cwd // "."' <<<"$input")
branch=$(git -C "$cwd" branch --show-current 2>/dev/null)
if [ -n "$branch" ] && [ "${#branch}" -gt 20 ]; then
  branch="${branch:0:20}…"
fi

sep="${DIM} · ${RESET}"

line="${MAGENTA}${model}${RESET}${sep}${YELLOW}${user}${RESET}${sep}${DIM}ctx ${RESET}${GREEN}${ctx_pct}%${RESET}${sep}${DIM}cache ${RESET}${cache_color}${cache_pct}%${cache_warn}${RESET}"

[ -n "$bar" ] && line="${line}${sep}${bar}"
[ -n "$effort" ] && line="${line}${sep}${DIM}effort ${RESET}${effort}"
[ -n "$branch" ] && line="${line}${sep}${DIM}${branch}${RESET}"

printf '%s' "$line"
