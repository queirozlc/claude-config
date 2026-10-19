import { expect, test } from 'claude-code/testing'

// No open ledger for the plugin folder: the prompt must pass through untouched.
test('prompt passes through when no ledger is open', async ($, on) => {
  let seen: unknown
  on('prompt.submit', (_$, e) => {
    seen = e
    return { text: e.text, context: e.context }
  })
  await $.prompt.submit({ text: 'hello' } as any)
  expect((seen as { context?: unknown }).context).toBeUndefined()
})
