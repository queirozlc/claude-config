import { expect, mock, test } from 'claude-code/testing'

const LEDGER = { key: 'EN-1', path: '/s/EN-1.md', phase: '4-execute', next: 'wait for Jon', master: 'Ned', routed: false, mtimeMs: 60000 }

// The engine beneath the plugin: a Maestri terminal, what ledger.py prints, and a file system in memory.
function world(on: any, ledgers = [LEDGER]) {
  const session = (sessionId: string, cwd: string) => JSON.stringify({ sessionId, cwd, status: 'idle', statusUpdatedAt: 0 })
  const files: Record<string, string> = {
    '/s/EN-1.md': '# EN-1 — cycle state\n\nPhase: 4-execute\n\n## Log\n\n- 16:02 dispatched Jon\n',
    '/home/u/.claude/sessions/1.json': session('sess-1', '/work/repo'),
    '/home/u/.claude/sessions/2.json': session('seat-1', '/work/repo/.maestri/roles/jon'),
    '/home/u/.claude/sessions/3.json': session('floor-1', '/work/.maestri/floors/repo--en-1/.maestri/roles/jon'),
    '/home/u/.claude/sessions/4.json': session('other-1', '/work/repo-two'),
    '/home/u/.claude/sessions/5.json': '',
  }
  on('fs.list', (_$: any, e: any) => ({
    value: Object.keys(files)
      .filter(p => p.startsWith(`${e.path}/`))
      .map(p => ({ name: p.slice(e.path.length + 1), kind: 'file', size: 1, mtimeMs: 0, isLink: false })),
  }))
  const clock = mock.clock(on)
  mock.env(on, { MAESTRI_TERMINAL_ID: 't', HOME: '/home/u' })
  on('process.run', () => ({
    value: { exitCode: 0, stdout: JSON.stringify({ project: 'p', seat: false, floor: null, branch: 'main', ledgers, problems: [] }), stderr: '', isStdoutTruncated: false, isStderrTruncated: false },
  }))
  on('session.cwd', () => ({ value: '/work/repo' }))
  on('session.id', () => ({ value: 'sess-1' }))
  on('fs.read', (_$: any, e: any) => {
    if (!(e.path in files)) throw new Error('ENOENT')
    return { value: files[e.path] }
  })
  on('fs.write', (_$: any, e: any) => {
    files[e.path] = e.text
    return { value: undefined }
  })
  return { files, clock }
}

const run = ($: any, args: string) => $.command.run({ command: 'ship-feedback', args })
const FILE = '/home/u/.agents/ship/feedback/p.md'

test('open cycle: the report is saved with the cycle and ledger context, and appended', async ($, on) => {
  const { files, clock } = world(on)
  await clock.set(180000)
  await run($, 'Jon stays idle after the dispatch')
  await run($, 'second report')
  const saved = files[FILE] ?? ''
  expect(saved).toContain('# Ship feedback: p')
  expect(saved).toContain('· EN-1')
  expect(saved).toContain('Jon stays idle after the dispatch')
  expect(saved).toContain('- Ledger EN-1: /s/EN-1.md')
  expect(saved).toContain('(2m before this report)')
  expect(saved).toContain('- 16:02 dispatched Jon')
  expect(saved).toContain('- Session: sess-1')
  expect(saved).toContain('- Live sessions: 3')
  expect(saved).toContain('sess-1 (this one) · idle for 3m · /work/repo')
  expect(saved).toContain('/home/u/.claude/projects/-work-repo--maestri-roles-jon/seat-1.jsonl')
  expect(saved).toContain('floor-1')
  expect(saved).not.toContain('other-1')
  expect(saved.split('\n## ').length - 1).toBe(2)
})

test('no open cycle: nothing is saved', async ($, on) => {
  const { files } = world(on, [])
  const out = await run($, 'a problem')
  expect(out.text).toContain('Nothing saved')
  expect(files[FILE]).toBeUndefined()
})
