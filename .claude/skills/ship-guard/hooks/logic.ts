import type { Scan } from '../types'

export const NONE: Scan = { project: null, seat: false, floor: null, branch: '', ledgers: [], problems: [] }

// A failure is a problem to show, never an empty answer: an empty answer looks like "no open cycle".
export const failed = (why: string): Scan => ({ ...NONE, problems: [`ledger.py did not run: ${why}`] })

export function parseScan(run: { exitCode: number; stdout: string; stderr: string }): Scan {
  if (run.exitCode !== 0) return failed(run.stderr.trim().split('\n').pop() || `exit ${run.exitCode}`)
  return JSON.parse(run.stdout)
}

// The line for a Maestro with no open ledger: it shows that the mod works and found none.
export const idleLine = (s: Scan) =>
  s.floor ? `ship: no open ledger names this floor (folder ${s.floor}, branch ${s.branch || 'none'})` : 'ship: no open cycle'
