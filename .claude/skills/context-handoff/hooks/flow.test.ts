import { expect, mock, test } from 'claude-code/testing'

// The band's text, or undefined when it does not show.
async function band($: any) {
  const ui = await $.ui.mount({ plugin: 'context-handoff', surface: 'terminal', component: 'AbovePrompt', props: { hasSurvey: false, isWorking: false, maxRows: 10 } })
  const text = await ui.find({ type: 'Text' })
  return text && `${text.props.color} ${text.text}`
}

const DONE = { answer: '', durationMs: 1, isAborted: false, turnId: 't', reason: 'answer' } as const

// The engine beneath the plugin: a Maestri terminal, and what ledger.py prints for its folder.
function world(on: any, { floor = null as string | null, master = '', open = true, seat = false, exitCode = 0, pct = 40 } = {}) {
  const w = { pct, mtime: 100, argv: [] as string[], prompts: [] as string[], commands: [] as string[], toasts: [] as string[], status: [] as unknown[] }
  const clock = mock.clock(on)
  mock.env(on, { MAESTRI_TERMINAL_ID: 't', HOME: '/home/u' })
  on('process.run', (_$: any, e: any) => {
    w.argv = e.argv
    const ledgers = open && !seat ? [{ key: '9', path: '/s/9.md', phase: '5-review', next: 'x', master, routed: false, mtimeMs: w.mtime }] : []
    const stdout = JSON.stringify({ project: 'p', seat, floor, branch: 'feat/9', ledgers, problems: [] })
    return { value: { exitCode, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('session.cwd', () => ({ value: '/work/repo' }))
  on('session.usage', () => ({ value: { startedAt: 0, context: { window: 1000, percent: w.pct }, rateLimits: [] } }))
  on('session.start', (_$: any, e: any) => ({ cwd: e.cwd }))
  on('turn.complete', (_$: any, e: any) => ({ text: e.answer }))
  on('ui.render', ($: any, e: any) => h($.ui.resolve(e).Box, {})) // the engine's empty band
  on('ui.status',(_$: any, e: any) => { w.status.push(e.text); return { value: undefined } })
  on('ui.toast', (_$: any, e: any) => { w.toasts.push(e.text); return { value: undefined } })
  on('prompt.submit', (_$: any, e: any) => { w.prompts.push(e.text); return { text: e.text } })
  on('command.run', (_$: any, e: any) => { w.commands.push(e.command); return {} })
  return { w, clock }
}

test('at the ceiling: handoff prompt, ledger changed, then /clear', { options: { autoClear: true } }, async ($, on) => {
  const { w, clock } = world(on)
  await $.turn.complete(DONE)
  await clock.advance(800)
  expect(w.argv).toEqual(['python3', '/home/u/.agents/ship/ledger.py', '/work/repo'])
  expect(w.prompts.length).toBe(1)
  expect(w.prompts[0]).toContain('Context handoff.')
  expect(w.prompts[0]).toContain('- /s/9.md')

  w.mtime = 200 // the Maestro wrote the ledger
  await $.turn.complete(DONE)
  await clock.advance(1500)
  expect(w.commands).toEqual(['clear'])
})

test('ledger not changed: no /clear, a toast says so', { options: { autoClear: true } }, async ($, on) => {
  const { w, clock } = world(on)
  await $.turn.complete(DONE)
  await clock.advance(800)
  await $.turn.complete(DONE) // handoff turn ended, ledger untouched
  await clock.advance(5000)
  expect(w.commands).toEqual([])
  expect(w.toasts.join()).toContain('did not update the ledger')
})

test('autoClear off: toast asks for /clear, no command', async ($, on) => {
  const { w, clock } = world(on)
  await $.turn.complete(DONE)
  await clock.advance(800)
  w.mtime = 200
  await $.turn.complete(DONE)
  await clock.advance(5000)
  expect(w.commands).toEqual([])
  expect(w.toasts.join()).toContain('Run /clear')
})

test('reload above the ceiling: session start sends the handoff, no turn needed', async ($, on) => {
  const { w, clock } = world(on)
  await $.session.start({ cwd: '/work/repo', surface: null, isInteractive: true })
  await clock.advance(1500)
  await clock.advance(800)
  expect(w.prompts.length).toBe(1)
})

test('below the ceiling: the band shows, nothing is sent', async ($, on) => {
  const low = world(on, { pct: 20 })
  await $.turn.complete(DONE)
  await low.clock.advance(5000)
  expect(await band($)).toBe('success ● ctx 20% · handoff at 35%')
  expect(low.w.prompts).toEqual([])
})

for (const [name, opts] of [
  ['seat', { seat: true }],
  ['no open ledger', { open: false }],
  ['ledger.py fails', { exitCode: 1 }],
] as const) {
  test(`${name}: no band, nothing is sent`, async ($, on) => {
    const none = world(on, opts as any)
    await $.turn.complete(DONE)
    await none.clock.advance(5000)
    expect(await band($)).toBeUndefined()
    expect(none.w.prompts).toEqual([])
  })
}

test('floor Maestro: handoff reports to the master, no /clear', { options: { autoClear: true } }, async ($, on) => {
  const f = world(on, { floor: 'support-agent--feat9', master: 'Ned Stark' })
  await $.turn.complete(DONE)
  await f.clock.advance(800)
  expect(f.w.prompts[0]).toContain('maestri ask "Ned Stark" "Context handoff written for 9.')

  f.w.mtime = 200
  await $.turn.complete(DONE)
  await f.clock.advance(5000)
  expect(f.w.commands).toEqual([])
  expect(f.w.toasts.join()).toContain('The master restarts this Maestro')
})
