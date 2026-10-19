import { expect, test } from 'claude-code/testing'

import { NONE, handoffPrompt, newest, parseScan, tone } from './logic'

test('tone goes green, yellow, red toward the ceiling', () => {
  expect(tone(10, 30)).toBe('success')
  expect(tone(18, 30)).toBe('warning')
  expect(tone(26, 30)).toBe('error')
  expect(tone(40, 30)).toBe('error')
})

const ledger = { key: '9', path: '/s/9.md', phase: '5-review', next: 'x', master: '', routed: false, mtimeMs: 100 }

test('a failed ledger.py run gives no ledgers', () => {
  expect(parseScan({ exitCode: 1, stdout: '' })).toEqual(NONE)
  expect(parseScan({ exitCode: 0, stdout: JSON.stringify({ ...NONE, ledgers: [ledger] }) }).ledgers[0]?.key).toBe('9')
})

test('newest is the last write of all ledgers', () => {
  expect(newest([])).toBe(0)
  expect(newest([ledger, { ...ledger, mtimeMs: 300 }])).toBe(300)
})

test('handoff prompt names the note and the clear mode', () => {
  expect(handoffPrompt(true, [ledger])).toContain('Handoff from <agent name> (<agent role>)')
  expect(handoffPrompt(true, [ledger])).toContain('clears itself')
  expect(handoffPrompt(false, [ledger])).toContain('run /clear')
})

test('a routed ledger gets a log line only, its floor Maestro owns the head', () => {
  expect(handoffPrompt(true, [ledger])).not.toContain('do not change its head')
  expect(handoffPrompt(true, [{ ...ledger, routed: true }])).toContain('/s/9.md (a floor cycle that you route: append one log line, do not change its head)')
})

test('on a floor the handoff prompt reports to the Master of the ledger head', () => {
  const l = { ...ledger, master: 'Dumbledore' }
  expect(handoffPrompt(false, [l], true)).toContain('maestri ask "Dumbledore" "Context handoff written for 9.')
  expect(handoffPrompt(false, [ledger], true)).toContain('the master named in your standing orders')
})
