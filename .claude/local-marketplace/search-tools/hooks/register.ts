import type { Register } from 'claude-code'

const RG = '/opt/homebrew/bin/rg'
const FD = '/opt/homebrew/bin/fd'
const LIMIT = 250

const GREP = {
  name: 'Grep',
  description: `Search file contents with ripgrep. ALWAYS use this tool to search code or text in files. NEVER run grep, rg, ag, perl -ne, sed -n or awk in Bash for searching: those need shell quoting, which fails on quotes, parentheses, $ and backslashes. Here the pattern is one argument, passed verbatim, so write it exactly as the regex.

When to use: find where a symbol is defined or called, find a string across the codebase, list the files that mention something, check if a pattern exists.
When not to use: reading a known file (use Read), finding files by name (use Glob), running a program (use Bash).

Pattern syntax is ripgrep (Rust regex): \\( for a literal parenthesis, \\. for a literal dot, \\w+ and \\d+ work, no lookaround. Use glob to restrict file types, e.g. "*.ts" or "*.{rb,erb}". Use files_only to get only paths. Respects .gitignore. Output is file:line:text, at most 50 matches per file and 250 lines in total; narrow with path or glob when it truncates.`,
  inputSchema: {
    type: 'object',
    properties: {
      pattern: { type: 'string', description: 'Ripgrep regex. Passed as one argument, no shell escaping needed.' },
      path: { type: 'string', description: 'File or directory to search. Default: project root.' },
      glob: { type: 'string', description: 'Only search files matching this glob, e.g. "*.tsx" or "*.{js,ts}".' },
      case_insensitive: { type: 'boolean', description: 'Ignore case. Default false.' },
      files_only: { type: 'boolean', description: 'Return matching file paths only, one per line.' },
      context: { type: 'integer', description: 'Lines of context before and after each match.' },
    },
    required: ['pattern'],
  },
}

const GLOB = {
  name: 'Glob',
  description: `Find files by name with a glob pattern. ALWAYS use this tool to locate files by name or extension. NEVER run find, fd, ls -R or tree in Bash for that: find has its own flag syntax and quoting rules, and the model gets them wrong.

When to use: locate a file whose name you know or partly know, list all files of one type, discover the layout of a directory.
When not to use: searching inside files (use Grep), listing one directory (use Bash ls).

Pattern examples: "**/*.tsx" every .tsx file; "src/**/*.test.ts" tests under src; "**/Dockerfile" by exact name; "**/*user*" by name fragment. Matched against the path relative to path. Respects .gitignore, skips .git. Returns one path per line, at most 250; narrow with path when it truncates.`,
  inputSchema: {
    type: 'object',
    properties: {
      pattern: { type: 'string', description: 'Glob pattern, e.g. "**/*.rb" or "app/models/*.rb".' },
      path: { type: 'string', description: 'Directory to search. Default: project root.' },
    },
    required: ['pattern'],
  },
}

const PROMPT = `# Search tools
Grep and Glob (mcp__search-tools__Grep, mcp__search-tools__Glob) are the search tools. Bash runs programs; it does not search.
Bad: Bash grep -rn "useState(" src/ --include="*.tsx"
Good: Grep { pattern: "useState\\(", path: "src", glob: "*.tsx" }
Bad: Bash find . -name "*.test.ts" -not -path "*/node_modules/*"
Good: Glob { pattern: "**/*.test.ts" }
Bad: Bash perl -ne 'print if /def \\w+\\(.*\\):/' lib/*.py
Good: Grep { pattern: "def \\w+\\(.*\\):", path: "lib", glob: "*.py" }
Bad: Bash rg -l "TODO" | head
Good: Grep { pattern: "TODO", files_only: true }
Bad: Bash ls -R app/models | grep user
Good: Glob { pattern: "**/*user*", path: "app/models" }`

export function grepArgs(e: Record<string, unknown>): string[] {
  const args = ['--no-heading', '--line-number', '--color', 'never', '--max-count', '50']
  if (e.case_insensitive) args.push('-i')
  if (e.files_only) args.push('-l')
  if (e.glob) args.push('-g', String(e.glob))
  if (typeof e.context === 'number' && e.context > 0) args.push('-C', String(e.context))
  args.push('-e', String(e.pattern), '--', String(e.path ?? '.'))
  return args
}

export function globArgs(e: Record<string, unknown>): string[] {
  const raw = String(e.pattern)
  // fd matches the glob against the full relative path; "**/" lets "src/*.ts" match "src/a.ts" and "./src/a.ts" alike.
  const pattern = raw.startsWith('**') || raw.startsWith('/') ? raw : '**/' + raw
  return ['--glob', '--full-path', '--color', 'never', '--type', 'f', '--', pattern, String(e.path ?? '.')]
}

export function cap(text: string): string {
  const lines = text.split('\n').filter(Boolean)
  const shown = lines.slice(0, LIMIT)
  return lines.length > LIMIT
    ? shown.join('\n') + `\n... ${lines.length - LIMIT} more lines. Narrow with path or glob.`
    : shown.join('\n')
}

export function render(run: { exitCode: number; stdout: string; stderr: string }, empty: string): string {
  if (run.exitCode > 1) return `search failed (${run.exitCode}): ${run.stderr.trim()}`
  return run.stdout.trim() ? cap(run.stdout) : empty
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.tool.register({ ...GREP, isDeferred: false })
    await $.tool.register({ ...GLOB, isDeferred: false })
    return next(e)
  })

  on('prompt.compose', async ($, e, next) => {
    const { sections } = await next(e)
    return { sections: [...sections, { id: 'search-tools:usage', text: PROMPT, scope: 'session' as const }] }
  })

  on('tool.call', { tool: 'mcp__search-tools__Grep' }, async ($, e) => {
    const run = await $.process.run([RG, ...grepArgs(e as Record<string, unknown>)], { timeoutMs: 30_000 })
    return { result: render(run, 'No matches.') }
  })

  on('tool.call', { tool: 'mcp__search-tools__Glob' }, async ($, e) => {
    const run = await $.process.run([FD, ...globArgs(e as Record<string, unknown>)], { timeoutMs: 30_000 })
    return { result: render(run, 'No files match.') }
  })
}
