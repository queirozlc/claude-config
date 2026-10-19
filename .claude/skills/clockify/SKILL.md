---
name: clockify
description: Register work time in Clockify with the `clockify` CLI. Use when the user asks to start or stop a timer, log time, log the standup, or check the day total for Enerflo work.
allowed-tools: Bash(clockify:*)
---

# clockify

`clockify` is a CLI at `~/.local/bin/clockify`. It writes time entries to the user's Clockify workspace, project `Enerflo`, billable. Run `clockify help` for the full command list. All times are the user's local time (America/Sao_Paulo).

## Commands

- `clockify status`: show the running timer
- `clockify start [text]`: start a timer now
- `clockify stop`: stop the running timer now (only one that the CLI started)
- `clockify rename "text" [ID]`: replace the text of the running timer (only one that the CLI started), or of entry ID. Times never change
- `clockify day` prints each entry's ID in brackets
- `clockify split ID "HH:MM:SS" "text"`: cut a stopped entry that the CLI created in two. The first part ends at HH:MM:SS and keeps its text. The second starts in the next minute, ends at the old end, and gets "text" with the same ticket. Split again for more parts. Use real split times from the cycle artifacts (ledger lines, report mtimes), never estimates. The CLI refuses entries the user made (it keeps a log of the IDs it created in `~/.local/state/clockify/created`)
- `clockify add "START" "END" [text]`: log a past entry. Format `YYYY-MM-DD HH:MM:SS`
- `clockify standup "END" ["DATE"]`: log the Platform Team Standup, 13:00:00 to END
- `clockify day ["DATE"]`: list the day's entries, the total, and a warning under 6h

## Team rules (the user's reviewers check these)

1. The Platform Team Standup runs every day from 13:00. The CLI reserves 13:00 to 13:35. No other entry may touch this window. Past standups ran 20 to 35 minutes.
2. Clockify compares times by the minute. Each entry starts in a later minute than the previous one ends. Leave a gap of a few minutes when the real work had one. The CLI refuses a conflict and names the entry.
3. Seconds are real. A timer from `start` and `stop` has true seconds. For `add` and `standup`, use exactly the times the user gave. Never round, invent, or adjust seconds or minutes to make an entry look better.
4. Descriptions are short, plain, and specific. Each one names the activity **and** its subject in this ticket: the feature, bug, file, behavior, or reviewer and comment. One line, no jargon. A phase label alone is never valid (`Addressing PR review comments`, `Investigating PR review comments`, `Planning the first implementation`). Never copy a text from another ticket or an example. Write it fresh from what this block does. Good: `Checking Fran's batch lookup suggestion on PR 7774`, `Browser testing the file upload field on partner`, `Reading deal files from cached plugin field values`. Test: a reader of the entry alone knows what was worked on.
5. No duplicate texts on the same day (a preference, not a hard rule). When the same kind of work starts again, say what this block does: `Fixing the error spacing from FE 2 review, wave 2`. Run `clockify day` before a start to see the texts already used.
6. If the running timer's text no longer matches the work, fix it at once with `clockify rename "<text>"`. A stopped entry that the CLI made is renamed only on the user's order: `clockify rename "<text>" <ID>`, with the ID from `clockify day`. The CLI keeps the times. Never rename an entry the user edited by hand.
7. The daily total should reach 6h. This is a check, not a target. Run `clockify day` near the end of the day. If the total is under 6h, report the gap once. Never add entries for work that did not happen.

## The user's entries are theirs

The user reviews every entry you add. The user also creates, edits, and deletes entries by hand.

- Never edit, move, stop, or delete an entry the user made. The CLI cannot do this. Do not use `curl` or another tool to do it.
- Never push back on a manual entry. Do not comment on its times, its text, its gaps, or its overlaps. Do not suggest a change to it.
- If the user edits or deletes an entry you made, accept it. Do not recreate it and do not log it again.
- `clockify stop` only stops a timer that the CLI started. If it refuses, report it in one line and leave the timer alone.
- If a new entry conflicts with a manual entry, the CLI refuses. Report the refusal as is and ask for new times. Do not suggest changing the manual entry.

## How to register time

1. Run `clockify status` first. A running timer blocks `start`. Run `clockify stop` first.
2. To start work: `CLOCKIFY_TICKET=EN-XXXX clockify start "<text>"`.
3. To end work: `clockify stop`.
4. For past work: use `clockify add` only with start and end times the user gave. If a time is missing, ask. Do not estimate.
5. For the standup: `clockify standup "HH:MM:SS"` with the end time the user gave.
6. Show the CLI output to the user after each write.

## How the user tracked before

- 4 to 7 entries a day, usually between 09:00 and 20:00. Daily totals ran from about 6h to 10h.
- One entry per block of work, per ticket. Gaps between entries were from 0 to 60 minutes.
- Project `Enerflo`, billable. Meetings that are not ticket work (1:1, internal sync) used the project `RAVN: Internal: Meetings`, not billable. The CLI does not write these entries. Tell the user if one is needed.
- The CLI builds `Enerflo: EN-1234 <text>`. The ticket key comes from `CLOCKIFY_TICKET` (for example `CLOCKIFY_TICKET=EN-5913 clockify start "<text>"`). Without it, the key comes from the git branch. Always set `CLOCKIFY_TICKET` when the current directory is not the ticket branch. Do not type the key or the `Enerflo:` prefix in the text.

## Safety

- The API key is in the macOS Keychain item `clockify-api-key`. Never read it, print it, or put it in a file, a command argument, or a message. Use only the `clockify` CLI.
- Entries are visible to the company and bill the client. Start, stop, and add only when the user asks.
- If the CLI prints an error, report it as is. Do not retry with other tools or with changed times.
- The CLI has no delete command. If an entry that the CLI made is wrong, tell the user. The user decides what to do.
