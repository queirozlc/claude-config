## Auth walls: human in the loop

**Prevention first.** A portal created in the Maestri UI with storage
**"Shared Globally"** keeps its LinkedIn session across restarts, so the wall
mostly does not appear. Everything below is the fallback for when the session
does eventually expire, not the normal path.

When it does happen, the hunt is **not autonomous** at that boundary, exactly
like `/ship` is not autonomous at the merge.

**The rule: an auth wall escalates to the human and the hunt keeps working.**
Never stop the whole run because one portal is locked. Never abandon a
half-finished dispatch. Park what is blocked, keep what is not.

### Detecting it

The source runner snapshots the portal and finds a login form, a checkpoint or
challenge page, or a "sign in to continue" interstitial instead of results.
`maestri portal info "<Portal>"` showing a `/login`, `/checkpoint/` or
`/authwall` URL is the same signal.

### First login, which the agent may perform

Credentials come from 1Password. Verified on 2026-09-01: the item is
`LinkedIn Lucas` in the `Personal` vault. `username` and `password` both
resolve. **There is no TOTP on the item**, which is correct: the second factor
is a confirmation the user approves on their phone.

```
op read "op://Personal/LinkedIn Lucas/username"
op read "op://Personal/LinkedIn Lucas/password"
```

The first `op read` in a session prompts Touch ID on the user's machine. That
prompt is expected; tell the user it is coming so they do not miss it.

**Handling rules, no exceptions:**

- Read the secret straight into the command that consumes it. Never write it
  to a file, never echo it, never put it in a ledger, a note, a log line, a
  report, or a `.out` file.
- Redirect the output of any command that could surface it.
- A password passed as a CLI argument is visible in the process table while it
  runs. That is a known limitation of the portal verbs and the reason the
  value must never also be persisted anywhere.
- If `op` is not signed in, do not work around it. Escalate.

### The wait, and why it is a background poll

After the agent submits the credentials, LinkedIn sends a confirmation to the
user's phone. **Only the user can clear that.** So:

1. `maestri notify "LinkedIn needs your confirmation on your phone. The hunt
is paused on the <Portal> portal and will resume by itself."`
2. Append to the ledger: `- HH:MM auth wall on <Portal>, awaiting user
confirmation`. Set **Open** to name it.
3. **Poll in the background.** Never block your foreground on a human. Use the
   harness background mechanism, poll every 20 to 30 seconds, and stop after
   15 minutes:

```
for i in $(seq 1 30); do
  maestri portal info "<Portal>" | grep -qiE 'login|checkpoint|authwall' || { echo AUTHED; break; }
  sleep 20
done
```

In Claude Code, run that with `run_in_background: true` and watch it with
`Monitor` or `TaskOutput`. 4. **While it polls, keep working.** Advance every application that does not
need that portal: tailoring, gating, fix rounds and packaging need no
portal at all. Only sourcing is blocked. 5. On `AUTHED`, log it and resume the blocked dispatch. On timeout, log the
timeout, set the ledger **Next** to the resume step, notify once more, and
stop cleanly. Do not re-notify on a loop.

### What never happens at an auth wall

- Never retry a password more than once. A second failure is a real problem,
  not a transient one, and repeated attempts lock the account.
- Never solve a CAPTCHA or an identity challenge. Escalate.
- Never switch to a different account.
- Never disable or bypass 2FA.

