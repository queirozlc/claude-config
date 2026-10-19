import type { OpenLedger, Scan } from '../types'

export const MARK = 'Context handoff.'

export const NONE: Scan = { project: null, seat: false, floor: null, branch: '', ledgers: [], problems: [] }

// ship-guard shows a failure of ledger.py. Here a failure means no handoff.
export function parseScan(run: { exitCode: number; stdout: string }): Scan {
  return run.exitCode === 0 ? JSON.parse(run.stdout) : NONE
}

// Green far from the ceiling, yellow from 60% of it, red from 85% of it.
export function tone(pct: number, ceiling: number): 'success' | 'warning' | 'error' {
  if (pct >= ceiling * 0.85) return 'error'
  return pct >= ceiling * 0.6 ? 'warning' : 'success'
}

export const newest =(ledgers: OpenLedger[]) => Math.max(0, ...ledgers.map(l => l.mtimeMs))

// A floor Maestro never clears itself: nobody prompts it afterwards. The master restarts it.
function lastStep(autoClear: boolean, ledgers: OpenLedger[], floor: boolean): string {
  if (!floor) return autoClear ? 'The session clears itself after this turn.' : 'Tell Lucas to run /clear.'
  const master = ledgers.find(l => l.master)?.master
  const to = master ? `"${master}"` : 'the master named in your standing orders'
  const keys = ledgers.map(l => l.key).join(', ')
  return `Tell the master in the background: \`maestri ask ${to} "Context handoff written for ${keys}. Restart me and send the handoff again."\` Do not run /clear.`
}

// The head of a routed ledger belongs to its floor Maestro: two writers on one head lose changes.
const ROUTED = ' (a floor cycle that you route: append one log line, do not change its head)'

export function handoffPrompt(autoClear: boolean, ledgers: OpenLedger[], floor = false): string {
  const files = ledgers.map(l => `- ${l.path}${l.routed ? ROUTED : ''}`).join('\n')
  return `${MARK} Your context reached its ceiling. Do these steps now and nothing else.
1. Update the head of each open ledger (Phase, Floor, Branch, PR, Ticket, Next, Open, Seats) and append one log line. Follow the ship skill state rules.
${files}
2. Load the maestri skill. Run \`maestri list\` to read your own agent name and role. Create one Maestri note: \`maestri note create --name "Handoff from <agent name> (<agent role>)" "<content>"\`. The content has: ledger paths, Phase, Next, Open items, each seat and whether it is clean or dirty, the sibling files to read first, and decisions not yet in the ledger. Maximum 40 lines.
3. Stop. Start no new work. ${lastStep(autoClear, ledgers, floor)}`
}
