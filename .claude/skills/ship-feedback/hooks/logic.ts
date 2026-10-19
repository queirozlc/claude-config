import type { Scan, Session } from '../types'

export const NONE: Scan = { project: null, seat: false, floor: null, branch: '', ledgers: [], problems: [] }

// A failure is a problem to show, never an empty answer: an empty answer looks like "no open cycle".
export const failed = (why: string): Scan => ({ ...NONE, problems: [`ledger.py did not run: ${why}`] })

export function parseScan(run: { exitCode: number; stdout: string; stderr: string }): Scan {
  if (run.exitCode !== 0) return failed(run.stderr.trim().split('\n').pop() || `exit ${run.exitCode}`)
  return JSON.parse(run.stdout)
}

export const stamp = (ms: number) => `${new Date(ms).toISOString().slice(0, 19)}Z`

export function age(ms: number) {
  const m = Math.max(0, Math.floor(ms / 60000))
  return m < 60 ? `${m}m` : `${Math.floor(m / 60)}h${m % 60}m`
}

export const logTail = (ledger: string, lines = 8) => (ledger.split('\n## Log')[1] ?? '').trim().split('\n').slice(-lines).join('\n')

export const count = (file: string) => file.split('\n## ').length - 1

// The live Claude Code sessions of the cycle, from ~/.claude/sessions/<pid>.json.
// A floor sees its own folder. The ground sees itself, its seats and every floor of the repo:
// Maestri keeps floors beside the repo, in .maestri/floors/<repo folder>--<branch>.
export function sessionsOf(all: Session[], cwd: string, floor: string | null) {
  const mark = `/.maestri/floors/${floor ?? `${cwd.split('/').pop()}--`}`
  return all.filter(s => s.cwd.includes(mark) || (!floor && (s.cwd === cwd || s.cwd.startsWith(`${cwd}/`))))
}

const transcript = (home: string, s: Session) => `${home}/.claude/projects/${s.cwd.replace(/[^a-zA-Z0-9]/g, '-')}/${s.sessionId}.jsonl`

// One entry of feedback/<project>.md. `tails` holds the last log lines of each ledger, by key.
export function entry(o: { at: number; text: string; scan: Scan; cwd: string; session: string; home: string; sessions: Session[]; tails: Record<string, string> }) {
  const s = o.scan
  const where = s.floor ? `floor ${s.floor}` : 'ground'
  return [
    `## ${stamp(o.at)} · ${s.ledgers.map(l => l.key).join(', ')}`,
    '',
    o.text,
    '',
    `- Where: ${where}, branch ${s.branch || 'none'}, ${o.cwd}`,
    `- Session: ${o.session}`,
    ...s.ledgers.flatMap(l => [
      `- Ledger ${l.key}: ${l.path}`,
      `  - Phase: ${l.phase}`,
      `  - Next: ${l.next}`,
      `  - Last write: ${stamp(l.mtimeMs)} (${age(o.at - l.mtimeMs)} before this report)`,
      ...(o.tails[l.key] ? ['  - Last log lines:', ...o.tails[l.key].split('\n').map(line => `    ${line}`)] : []),
    ]),
    `- Live sessions: ${o.sessions.length}`,
    ...o.sessions.flatMap(x => [
      `  - ${x.sessionId}${x.sessionId === o.session ? ' (this one)' : ''} · ${x.status ?? 'unknown'} for ${age(o.at - (x.statusUpdatedAt ?? o.at))} · ${x.cwd}`,
      `    ${transcript(o.home, x)}`,
    ]),
    '',
    '',
  ].join('\n')
}
