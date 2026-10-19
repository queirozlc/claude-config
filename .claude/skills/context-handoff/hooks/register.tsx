import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Scan, Stage } from '../types'
import { NONE, handoffPrompt, newest, parseScan, tone } from './logic'

const stage = atom({ plugin: 'context-handoff', key: 'stage' } as const, 'idle' as Stage)
const mark = atom({ plugin: 'context-handoff', key: 'mark' } as const, 0)
// The band's value. null: no open ledger, no band.
const shown = atom({ plugin: 'context-handoff', key: 'pct' } as const, null as number | null)

const usage = async ($: any) => (await $.session.usage()).context.percent ?? 0

// ~/.agents/ship/ledger.py is the one reader of ledgers. The Stop hooks and ship-guard use it too.
// It answers the open ledgers of this agent's cycle, only for a Maestro in a Maestri terminal.
async function scan($: any): Promise<Scan> {
  try {
    if (!(await $.env.get('MAESTRI_TERMINAL_ID'))) return NONE
    const reader = `${await $.env.get('HOME')}/.agents/ship/ledger.py`
    return parseScan(await $.process.run(['python3', reader, await $.session.cwd()]))
  } catch {
    return NONE
  }
}

async function tick($: any, ceiling: number, autoClearOption: boolean) {
  const found = await scan($)
  const floor = found.floor !== null
  const autoClear = autoClearOption && !floor
  const ledgers = found.ledgers
  if (!ledgers.length) return update($, shown, () => null)
  const pct = await usage($)
  await update($, shown, () => pct)

  const s = await read($, stage)
  if (s === 'idle' && pct >= ceiling) {
    const before = newest(ledgers)
    await update($, mark, () => before)
    await update($, stage, () => 'sent')
    // Outside this dispatch: the prompt waits for an idle session.
    $.clock.after(800, () => {
      // The call resolves as the handoff turn starts: the next turn.complete is that turn's.
      $.prompt
        .submit({ text: handoffPrompt(autoClear, ledgers, floor) })
        .then(() => update($, stage, () => 'running'))
        .catch(() => update($, stage, () => 'failed'))
    })
  } else if (s === 'running') {
    // Safety check: no ledger change, no clear.
    if (newest(ledgers) > (await read($, mark))) {
      await update($, stage, () => 'done')
      if (autoClear) {
        $.ui.toast('Handoff saved. Clearing.')
        $.clock.after(1500, () => {
          $.command.run({ command: 'clear' }).catch(() => $.ui.toast('Could not run /clear. Run it yourself.'))
        })
      } else {
        $.ui.toast(floor ? 'Handoff saved. The master restarts this Maestro.' : 'Handoff saved. Run /clear.', { timeoutMs: 15000 })
      }
    } else {
      await update($, stage, () => 'failed')
      $.ui.toast('Handoff did not update the ledger. No clear. Check it.', { timeoutMs: 15000 })
    }
  } else if ((s === 'done' || s === 'failed') && pct < ceiling - 5) {
    await update($, stage, () => 'idle')
  }
}

export const register: Register = (on, options) => {
  const ceiling = Number(options.ceilingPercent ?? 35)
  const autoClear = options.autoClear === true

  on('turn.complete', async ($, e, next) => {
    const out = await next(e)
    await tick($, ceiling, autoClear)
    return out
  })

  // Live value between turns. The ledger scan stays on turn.complete.
  on('tool.call', async ($, e, next) => {
    const out = await next(e)
    try {
      if ((await read($, shown)) !== null) {
        const pct = await usage($)
        await update($, shown, () => pct)
      }
    } catch {}
    return out
  })

  on('ui.render', { component: 'AbovePrompt' }, async ($, e, next) => {
    const pct = await read($, shown)
    if (pct === null || e.props.hasSurvey) return next(e)
    const { Text } = $.ui.resolve(e)
    return <Text color={tone(pct, ceiling)}>● ctx {pct}% · handoff at {ceiling}%</Text>
  })

  // A reload fires this too. It drops the timers but keeps the state: a handoff in flight would stay stuck.
  on('session.start', async ($, e, next) => {
    const s = await read($, stage)
    if (s === 'sent' || s === 'running') await update($, stage, () => 'idle')
    $.clock.after(1500, () => {
      tick($, ceiling, autoClear)
    })
    return next(e)
  })

  // The context is empty again, the cycle can hand off again later.
  on('session.end', async ($, e, next) => {
    if (e.reason === 'clear') await update($, stage, () => 'idle')
    return next(e)
  })
}
