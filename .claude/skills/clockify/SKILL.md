---
name: clockify
description: Register work time in Clockify with the `clockify` CLI. Use when the user asks to start or stop a timer, log time, log the standup, or check the day total for Enerflo work. Also use when a clockify hook asks about a missing or stale timer.
allowed-tools: Bash(clockify:*)
---

# clockify

`clockify` writes time entries to the user's Clockify workspace, project `Enerflo`, billable. All times are local (America/Sao_Paulo). Run `clockify help` or `clockify help <command>` for details.

## Commands

- `clockify status`: one line, `running <id> <HH:MM:SS> <elapsed> <description>` or `no timer running`
- `clockify day ["YYYY-MM-DD"]`: tsv `start end dur id description`, then `# total ...` and `# warning: below the 6h daily minimum ...`. The id is what `rename` and `split` take
- `clockify start [text]`: start a timer now
- `clockify stop`: stop the running timer now (only one the CLI started)
- `clockify rename "text" [ID]`: replace the text of the running timer (only one the CLI started), or of entry ID (only one the CLI created). Times never change
- `clockify split ID "HH:MM:SS" "text"`: cut a stopped entry that the CLI created in two. The first part ends at HH:MM:SS and keeps its text. The second starts in the next minute, ends at the old end, and gets "text" with the same ticket. Split again for more parts. Use real split times from the cycle artifacts (ledger lines, report mtimes), never estimates
- `clockify add "START" "END" [text]`: log a past entry. Format `YYYY-MM-DD HH:MM:SS` (`HH:MM` means seconds 00)
- `clockify standup "END" ["DATE"]`: log the Platform Team Standup, 13:00:00 to END

Writes print one line: `started|stopped|added|renamed|split <id> <start>-<end> <description>`, plus a `warning:` line when needed. Errors print `error:` and `fix:` on stderr. Exit codes: 0 ok, 1 usage, 2 rule refused (conflict, standup, not created by this CLI), 3 auth/keychain, 4 network/API.

The CLI builds `Enerflo: EN-1234 <text>`. The ticket comes from `CLOCKIFY_TICKET`, else the git branch. Always set `CLOCKIFY_TICKET=EN-XXXX` when the current directory is not the ticket branch. Do not type the key or the `Enerflo:` prefix in the text.

## Team rules (the user's reviewers check these)

1. The Platform Team Standup runs every day from 13:00. The CLI reserves 13:00 to 13:35. No other entry may touch this window. Past standups ran 20 to 35 minutes.
2. Clockify compares times by the minute. Each entry starts in a later minute than the previous one ends. Leave a gap of a few minutes when the real work had one. The CLI refuses a conflict and names the entry.
3. Seconds are real. A timer from `start` and `stop` has true seconds. For `add` and `standup`, use exactly the times the user gave. Never round, invent, or adjust seconds or minutes to make an entry look better.
4. Descriptions are short, plain, and specific. Each one names the activity and its subject in this ticket: the feature, bug, file, behavior, or reviewer and comment. One line, no jargon. A phase label alone is never valid (`Addressing PR review comments`, `Investigating PR review comments`, `Planning the first implementation`). Never copy a text from another ticket or an example. Write it fresh from what this block does. Good: `Checking Fran's batch lookup suggestion on PR 7774`, `Browser testing the file upload field on partner`, `Reading deal files from cached plugin field values`. Test: a reader of the entry alone knows what was worked on.
5. No duplicate texts on the same day (a preference, not a hard rule). When the same kind of work starts again, say what this block does: `Fixing the error spacing from FE 2 review, wave 2`. Run `clockify day` before a start to see the texts already used.
6. If the running timer's text no longer matches the work, fix it at once with `clockify rename "<text>"`. A stopped entry that the CLI made is renamed only on the user's order: `clockify rename "<text>" <ID>`. Never rename an entry the user edited by hand.
7. The daily total should reach 6h. This is a check, not a target. Run `clockify day` near the end of the day. If the total is under 6h, report the gap once. Never add entries for work that did not happen.

## The user's entries are theirs

The user reviews every entry you add. The user also creates, edits, and deletes entries by hand.

- Never edit, move, stop, or delete an entry the user made. The CLI cannot do this (it keeps the ids it created in `~/.local/state/clockify/`). Do not use `curl` or another tool to do it.
- Never push back on a manual entry. Do not comment on its times, text, gaps, or overlaps. Do not suggest a change to it.
- If the user edits or deletes an entry you made, accept it. Do not recreate it and do not log it again.
- `clockify stop` only stops a timer that the CLI started. If it refuses, report it in one line and leave the timer alone.
- If a new entry conflicts with a manual entry, the CLI refuses. Report the refusal as is and ask for new times. Do not suggest changing the manual entry.

## How to register time

1. Run `clockify status` first. A running timer blocks `start`. Run `clockify stop` first.
2. To start work: `CLOCKIFY_TICKET=EN-XXXX clockify start "<text>"`.
3. To end work: `clockify stop`.
4. For past work: `clockify add` with start and end times the user gave. If a time is missing, ask. Do not estimate. Exception: in a ship cycle, backfill untracked work without asking, using real times from the cycle artifacts (ledger lines, report mtimes).
5. For the standup: `clockify standup "HH:MM:SS"` with the end time the user gave.
6. Show the CLI output to the user after each write.

## Ship cycle

Only the ground Maestro runs `clockify`. Floor Maestros and seats never do. Keep one timer for the whole cycle, one entry per phase: `stop`, wait for the next clock minute, then `start`. Ledger phase `6-awaiting-merge-permission` means no timer. Resume check: run `clockify status` on the first message of a day or session, after `/clear` or a handoff, and on every message about an open ticket. If ticket work ran with no timer, backfill from the first proven time, then start a timer for the work now. Before 13:00, tell the user if the running timer would cross the standup. Do not stop it alone. If a command refuses, report it in one line and go on without the timer.

## Hooks

`clockify hook install` adds two hooks to `.claude/settings.local.json`. They only read `status` and never write to Clockify.

- Prompt hook: adds a `clockify:` context line with the timer state and the ticket. It also reports an idle gap (timer ran through more than 30 minutes of silence) and a running timer before the 13:00 standup.
- Stop hook: after a turn that edited files or ran agents with no timer, it blocks once (at most every 20 minutes per session).
- Obey them: with no timer and ticket work, start one with a specific text, or backfill from the first proven time, or say in one line why no timer applies. For an idle gap, report it and suggest `stop` plus a backfill or `split`. Never fix it alone.
- `CLOCKIFY_HOOK=off` silences them. They act only for the timer owner.

## How the user tracked before

- 4 to 7 entries a day, usually between 09:00 and 20:00. Daily totals ran from about 6h to 10h.
- One entry per block of work, per ticket. Gaps between entries were from 0 to 60 minutes.
- Project `Enerflo`, billable. Meetings that are not ticket work (1:1, internal sync) used the project `RAVN: Internal: Meetings`, not billable. The CLI does not write these entries. Tell the user if one is needed.

## Safety

- The API key is in the macOS Keychain item `clockify-api-key`. Never read it, print it, or put it in a file, a command argument, or a message. Use only the `clockify` CLI.
- Entries are visible to the company and bill the client. Start, stop, and add only when the user asks, or as the ship cycle and the hooks above require.
- If the CLI prints an error, report it as is. Do not retry with other tools or with changed times.
- The CLI has no delete command. If an entry that the CLI made is wrong, tell the user. The user decides what to do.
