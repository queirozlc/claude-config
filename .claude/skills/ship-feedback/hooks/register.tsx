import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Scan, Session, View } from '../types'
import { NONE, age, count, entry, failed, logTail, parseScan, sessionsOf } from './logic'

const PANE = 'ship-feedback'
const view = atom({ plugin: 'ship-feedback', key: 'view' } as const, { scan: NONE, now: 0, file: '', saved: 0 } as View)

// ~/.agents/ship/ledger.py is the one reader of ledgers. ship-guard and context-handoff use it too.
async function scan($: any): Promise<Scan> {
  try {
    if (!(await $.env.get('MAESTRI_TERMINAL_ID'))) return NONE
    const reader = `${await $.env.get('HOME')}/.agents/ship/ledger.py`
    return parseScan(await $.process.run(['python3', reader, await $.session.cwd()]))
  } catch (err) {
    return failed((err as Error).message)
  }
}

const readOr = ($: any, path: string, or: string): Promise<string> => $.fs.read(path).catch(() => or)

// A file that does not parse is a session that just ended: skip it.
async function liveSessions($: any, home: string): Promise<Session[]> {
  const dir = `${home}/.claude/sessions`
  const names: { name: string }[] = await $.fs.list(dir).catch(() => [])
  const read = names.filter(n => n.name.endsWith('.json')).map(n => readOr($, `${dir}/${n.name}`, '').then(t => JSON.parse(t)).catch(() => null))
  return (await Promise.all(read)).filter(Boolean)
}

async function refresh($: any) {
  const found = await scan($)
  const file = `${await $.env.get('HOME')}/.agents/ship/feedback/${found.project ?? 'unknown'}.md`
  const next: View = { scan: found, now: await $.clock.now(), file, saved: count(await readOr($, file, '')) }
  await update($, view, () => next)
  return next
}

const isOpen = async ($: any) => (await $.ui.panes()).some((p: { id: string }) => p.id === PANE)

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'ship-feedback',
      description: 'Save a problem with the open /ship cycle: /ship-feedback <what went wrong>. No text: toggle the pane',
    })
    // The pane shows how long the ledger is idle: it must move while no turn runs.
    $.clock.every(30000, () => {
      isOpen($).then(open => open && refresh($))
    })
    return next(e)
  })

  on('command.run', { command: 'ship-feedback' }, async ($, e) => {
    const v = await refresh($)
    const s = v.scan
    if (!s.ledgers.length) return { text: `${s.problems[0] ?? 'No open /ship cycle here'}. Nothing saved.` }

    const text = e.args.trim()
    if (!text) {
      if (await isOpen($)) {
        await $.ui.close({ id: PANE })
        return { text: 'Pane closed.' }
      }
      await $.ui.open({ id: PANE, title: 'Ship feedback' })
      return { text: 'Pane opened. Save a report with /ship-feedback <what went wrong>.' }
    }

    const tails: Record<string, string> = {}
    for (const l of s.ledgers) tails[l.key] = logTail(await readOr($, l.path, ''))
    const home = await $.env.get('HOME')
    const cwd = await $.session.cwd()
    const sessions = sessionsOf(await liveSessions($, home), cwd, s.floor)
    const old = await readOr($, v.file, `# Ship feedback: ${s.project}\n\n`)
    await $.fs.write(v.file, old + entry({ at: v.now, text, scan: s, cwd, session: await $.session.id(), home, sessions, tails }))
    await update($, view, () => ({ ...v, saved: v.saved + 1 }))
    return { text: `Saved to ${v.file} (${s.ledgers.map(l => l.key).join(', ')}, ${sessions.length} live sessions).` }
  })

  on('turn.complete', async ($, e, next) => {
    const out = await next(e)
    if (await isOpen($)) await refresh($)
    return out
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const v = await read($, view)
    const s = v.scan
    return (
      <Box flexDirection="column">
        {s.problems.map(p => (
          <Text color="red">{p}</Text>
        ))}
        {!s.ledgers.length && <Text dimColor>No open cycle.</Text>}
        {s.ledgers.map(l => (
          <Box flexDirection="column" marginBottom={1}>
            <Text bold>{l.key}</Text>
            <Text>Phase: {l.phase}</Text>
            <Text>Next: {l.next}</Text>
            <Text color={v.now - l.mtimeMs > 600000 ? 'yellow' : undefined}>Ledger idle: {age(v.now - l.mtimeMs)}</Text>
            <Text dimColor>{l.path}</Text>
          </Box>
        ))}
        <Text dimColor>{s.floor ? `floor ${s.floor}` : 'ground'} · {s.branch || 'no branch'}</Text>
        <Text dimColor>{v.saved} report(s) in {v.file}</Text>
      </Box>
    )
  })
}
