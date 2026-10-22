import { expect, mock, test } from 'claude-code/testing'

const DONE = { answer: '', durationMs: 1, isAborted: false, turnId: 't', reason: 'answer' } as const

// An open ledger, and a plugin beneath that draws its own line in the band.
test('open cycle: the band keeps the line of the plugin beneath', async ($, on) => {
  mock.env(on, { MAESTRI_TERMINAL_ID: 't', HOME: '/home/u' })
  on('process.run', () => {
    const ledgers = [{ key: '9', path: '/s/9.md', phase: '5-review', next: 'x', master: '', routed: false, mtimeMs: 1 }]
    const stdout = JSON.stringify({ project: 'p', seat: false, floor: null, branch: 'feat/9', ledgers, problems: [] })
    return { value: { exitCode: 0, stdout, stderr: '', isStdoutTruncated: false, isStderrTruncated: false } }
  })
  on('session.cwd', () => ({ value: '/work/repo' }))
  on('turn.complete', (_$: any, e: any) => ({ text: e.answer }))
  on('ui.render', ($: any, e: any) => h($.ui.resolve(e).Text, {}, 'ctx 12%'))

  await $.turn.complete(DONE)
  const ui = await $.ui.mount({ plugin: 'ship-guard', surface: 'terminal', component: 'AbovePrompt', props: { hasSurvey: false, isWorking: false, maxRows: 10 } })
  const texts = (await ui.findAll({ type: 'Text' })).map((t: any) => t.text)
  expect(texts.some((t: string) => t.includes('open cycle 9'))).toBe(true)
  expect(texts).toContain('ctx 12%')
})
