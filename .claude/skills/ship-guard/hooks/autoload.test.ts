import { expect, mock, test } from 'claude-code/testing'

const LEDGER = { key: '9', path: '/s/9.md', phase: '4-execute', next: 'wait for Jon', master: 'Ned', routed: false, mtimeMs: 1 }

// The engine beneath the plugin: a Maestri terminal, and what ledger.py prints for its folder.
function world(on: any, { ledgers = [LEDGER], seat = false, exitCode = 0, terminal = 't' } = {}) {
  const w = { argv: [] as string[], commands: [] as { command: string; args: string }[], context: undefined as unknown }
  const clock = mock.clock(on)
  mock.env(on, { MAESTRI_TERMINAL_ID: terminal, HOME: '/home/u' })
  on('process.run', (_$: any, e: any) => {
    w.argv = e.argv
    const stdout = JSON.stringify({ project: 'p', seat, floor: null, branch: 'main', ledgers: seat ? [] : ledgers, problems: [] })
    return { value: { exitCode, stdout, stderr: 'python3: not found', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('session.cwd', () => ({ value: '/work/repo' }))
  on('session.start', (_$: any, e: any) => ({ cwd: e.cwd }))
  on('session.end', (_$: any, e: any) => ({ sessionId: e.sessionId }))
  on('skill.prompt', (_$: any, e: any) => ({ text: e.text }))
  on('prompt.submit', (_$: any, e: any) => { w.context = e.context; return { text: e.text, context: e.context } })
  on('ui.toast', () => ({ value: undefined }))
  on('command.run', (_$: any, e: any) => { w.commands.push({ command: e.command, args: e.args }); return {} })
  return { w, clock }
}

const START = { cwd: '/work/repo', surface: 'terminal', isInteractive: true } as const
const CLEAR = { reason: 'clear', sessionId: 's', resume: {} } as any

test('session start: ledger.py reads the folder, /ship runs by itself, once', async ($, on) => {
  const { w, clock } = world(on)
  await $.session.start(START)
  await clock.advance(1500)
  expect(w.argv).toEqual(['python3', '/home/u/.agents/ship/ledger.py', '/work/repo'])
  expect(w.commands.map(c => c.command)).toEqual(['ship'])
  expect(w.commands[0]?.args).toContain('Handoff from')
  await clock.advance(5000)
  expect(w.commands.length).toBe(1)
})

test('after /clear: /ship runs again', async ($, on) => {
  const { w, clock } = world(on)
  await $.session.start(START)
  await clock.advance(1500)
  await $.session.end(CLEAR)
  await clock.advance(1500)
  expect(w.commands.map(c => c.command)).toEqual(['ship', 'ship'])
})

test('ship already loaded: no command', async ($, on) => {
  const { w, clock } = world(on)
  await $.skill.prompt({ skill: 'ship', text: '' })
  await $.session.start(START)
  await clock.advance(5000)
  expect(w.commands).toEqual([])
})

test('not loaded: the prompt carries the order to load the skill, with a number key', async ($, on) => {
  const { w } = world(on)
  await $.prompt.submit({ text: 'hello' } as any)
  expect(JSON.stringify(w.context)).toContain('- 9 (Phase: 4-execute) Next: wait for Jon')
})

for (const [name, opts] of [
  ['seat', { seat: true }],
  ['no open ledger', { ledgers: [] }],
  ['not a Maestri terminal', { terminal: '' }],
  ['ledger.py fails', { exitCode: 1 }],
] as const) {
  test(`${name}: no command, the prompt passes through`, async ($, on) => {
    const { w, clock } = world(on, opts as any)
    await $.session.start(START)
    await clock.advance(5000)
    await $.prompt.submit({ text: 'hello' } as any)
    expect(w.commands).toEqual([])
    expect(w.context).toBeUndefined()
  })
}
