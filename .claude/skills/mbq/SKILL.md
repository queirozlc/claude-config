---
name: mbq
description: Query the Enerflo database through Metabase with the read-only mbq CLI. Use when asked to query the Enerflo database or Metabase, check production or staging data, count rows, inspect tables or columns, or compare data between environments.
---

# mbq: read-only Enerflo Metabase CLI

Use it to answer data questions with SELECT queries. It never writes. Run `mbq help` and `mbq help sql` for details.

## Databases

5 V2 (prod), 6 V2 (Staging), 8 Legacy (mysql), 9 Legacy (Staging), 4 Segment, 10 Enerflo Data Lake (athena).
Explore on 6. Query 5 only when the question is about production. Run `mbq dbs` to confirm ids.

## Workflow

1. Find the table: `mbq tables 6 --like 'deal%'`
2. Read its columns: `mbq columns 6 deal` (add `--schema public` if names clash)
3. Query with a small `--limit`: `mbq sql 6 "select id, status from deal order by updated_at desc limit 5"`
4. Compare environments: `mbq sql 5,6 "select count(*) as n from deal"` prints one `## db <id> <name>` block each.

## Output

Default is tsv: header line, one row per line, `NULL` for nulls, long cells cut with `…[+N]`.
The last line is a `#` footer: row count, db, time, and a note if `--limit` cut rows (default 100, `--limit 0` = all, Metabase caps at 2000).
Aggregate in SQL (count, group by) instead of fetching many rows. Select only the columns you need.
Other formats: `--format json` (`{cols,rows,note}`, footer in `note`), `jsonl` and `csv` (no footer, parse as is), `table`. Use `--max-cell 0` to see full cell values.

## Read-only rule

One SELECT or `WITH ... SELECT`, no `;`. Write words (insert, update, delete, drop, create, into, copy, lock, ...) and side-effect functions are rejected, also inside strings. Never try to work around the guard or send write SQL, not even to test it.

## Errors

Printed on stderr as `error:` and `fix:`. Exit codes: 1 query or usage error, 2 guard rejected, 3 auth, 4 network.
Exit 3 (no session or expired): stop and ask the user to run `mbq login`. Do not retry.
Exit 4: check the VPN or network, then retry once.
