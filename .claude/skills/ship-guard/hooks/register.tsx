import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Scan } from '../types'
import { NONE, failed, idleLine, parseScan } from './logic'

const isLoaded = atom({ plugin: 'ship-guard', key: 'isLoaded' } as const, false)
const tried = atom({ plugin: 'ship-guard', key: 'tried' } as const, false)
const last = atom({ plugin: 'ship-guard', key: 'scan' } as const, NONE as Scan)

// ~/.agents/ship/ledger.py is the one reader of ledgers. The Stop hooks and context-handoff use it too.
async function scan($: any): Promise<Scan> {
  try {
    if (!(await $.env.get('MAESTRI_TERMINAL_ID'))) return NONE
    const reader = `${await $.env.get('HOME')}/.agents/ship/ledger.py`
    return parseScan(await $.process.run(['python3', reader, await $.session.cwd()]))
  } catch (err) {
    return failed((err as Error).message)
  }
}

async function refresh($: any) {
  const found = await scan($)
  await update($, last, () => found)
  return found
}

// Runs /ship once per context. If the command fails, the prompt note still forces the load.
async function autoLoad($: any) {
  const found = await refresh($)
  if (!found.ledgers.length || (await read($, isLoaded)) || (await read($, tried))) return
  await update($, tried, () => true)
  $.command
    .run({ command: 'ship', args: 'resume the open cycle from its ledger. If `maestri list` shows a note named "Handoff from ...", read it too.' })
    .catch(() => $.ui.toast('ship-guard: could not run /ship. Type /ship.'))
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    $.clock.after(1500, () => {
      autoLoad($)
    })
    return next(e)
  })

  // /clear fires no session.start: reset here, the context is empty again.
  on('session.end', async ($, e, next) => {
    if (e.reason === 'clear') {
      await update($, isLoaded, () => false)
      await update($, tried, () => false)
      $.clock.after(1500, () => {
        autoLoad($)
      })
    }
    return next(e)
  })

  // Typed /ship or loaded through the Skill tool: same event.
  on('skill.prompt', { skill: 'ship' }, async ($, e, next) => {
    await update($, isLoaded, () => true)
    return next(e)
  })

  // Force: until the skill is loaded, every prompt carries the order to load it.
  on('prompt.submit', async ($, e, next) => {
    if (await read($, isLoaded)) return next(e)
    const found = (await refresh($)).ledgers
    if (!found.length || /^\s*\/ship\b/.test(e.text)) return next(e)
    const list = found.map(l => `- ${l.key} (Phase: ${l.phase}) Next: ${l.next}`).join('\n')
    return next({
      ...e,
      context: [
        ...(e.context ?? []),
        `ship-guard: open /ship cycle ledger(s) exist for this repo and the ship skill is NOT loaded in this context.\n${list}\nBefore anything else, load the ship skill with the Skill tool and follow its resume rule. Then answer the user's message.`,
      ],
    })
  })

  // A turn can open, close or break a ledger: the band follows.
  on('turn.complete', async ($, e, next) => {
    const out = await next(e)
    await refresh($)
    return out
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const s = await read($, last)
    if (e.props.hasSurvey || s.seat || (!s.project && !s.problems.length)) return next(e)
    const { Box, Text } = $.ui.resolve(e)
    const keys = s.ledgers.map(l => l.key).join(', ')
    const loaded = await read($, isLoaded)
    // The band has one tree: carry the plugins beneath (context-handoff's ctx line) inside it.
    const below = await next(e)
    return (
      <Box flexDirection="column">
        {s.problems.map(p => (
          <Text color="red">ship: {p}</Text>
        ))}
        {!keys ? (
          <Text dimColor>{idleLine(s)}</Text>
        ) : loaded ? (
          <Text dimColor>ship: loaded ({keys})</Text>
        ) : (
          <Text color="red">ship: NOT loaded, open cycle {keys}. Loading it now.</Text>
        )}
        {below}
      </Box>
    )
  })
}
