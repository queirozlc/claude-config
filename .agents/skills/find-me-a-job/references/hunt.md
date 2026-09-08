## The hunt

### 0. Assemble

`maestri list`. Fill the config's seat table. Swap the required seats in place
with `--replace`, recruit approved missing seats, and verify the four portal
names used by the scripts. Create the hunt ledger. Do not recruit Kestrel
unless the source runner later reports a parser failure.

**Base check.** Read `~/career/resumes/base-en.tex`. If its bullets do not
follow the voice rule in `CV-SPEC.md` (first person, past tense, subject
omitted; `I` in the Summary), dispatch a base round to the Architect and a
File Readability Check plus Recruiter Readability Score run to the Analyzer before any tailoring. A tailored CV
copies the base; a wrong base makes every tailored CV wrong. Sourcing does
not depend on the base, so start the deterministic source runner at the same time.

### 1. Source

Run `scripts/linkedin_source.py` directly with the hunt query config. It drives
up to three isolated portals in parallel and writes `events.jsonl`, a live
`preflight.jsonl` triage queue, evidence files, and atomic
`run.complete.json` under `state/source-<hunt-id>/`. Keep the exec session
attached. This runner is the primary source path.

Watch `preflight.jsonl` while the source process runs. Triage each new record
as soon as it appears. Do not wait for `run.complete.json`. Start an accepted
application immediately under `auto-advance`. The completion sentinel means
all source workers stopped. `events.jsonl` remains the audit record.

Use the Market Scout only when the runner records a parser failure for a
specific LinkedIn layout. The fallback dispatch handles only that surface and
query. It does not repeat completed queries. Every fallback prompt carries the
segment weighting, recency cut, query, portal, report path, and exact failed
runner event.

**A run is a boolean query string typed into the LinkedIn search box**, per
the Sourcing section of `~/career/find-me-a-job.md`, for example
`("typescript" or "node.js") AND "senior" AND "latam"`. Filters (date,
remote) are applied after the query, through the UI. Browsing the Jobs tab
or Posts tab with filters alone is not a run and yields noise.

**The source runner captures, it never triages.** The
only capture filters are the recency cut, a remote or LatAm location, and a
stack token in the text. Employment type, contract type, company origin and
seniority are data to capture, never grounds to drop a posting. Dropping
"Full-time" postings loses US-direct contractor roles, which are
labelled Full-time on LinkedIn more often than not. `f_SAL` on a Jobs URL is
the salary filter, not Remote.

The source record includes the full observed posting evidence. The Maestro
records **posting language** and **company origin** during intake and uses both
to pick the CV language.

**The recency cut is not negotiable.** Past 24 hours first. Past week is the
widest acceptable window. A posting older than that usually has candidates in
final stages. If a surface returns nothing inside the cut, that is a valid
result; report it and do not widen the window to manufacture volume.

The source runner records the exact repost and competition labels. It does not hide or
normalize them. A missing applicant or Apply-click count is `not observable`.

The Maestro writes accepted raw results to `~/career/jobs/` and appends each run to
`~/career/keywords/search-log.md` with the exact query string. A run without
its exact query string is not reproducible and was wasted.

### 2. Triage (you, the Maestro)

You do this yourself. It is judgement, not labour. **It is never skipped.** A
raw list that becomes the shortlist unchanged is a triage that did not run.

First apply the config's **triage knockouts** and drop every hit:

- Any role labeled `Reposted`.
- Any role that states `Over 100 applicants`, `100+ applicants`, or more than
  100 people clicked Apply. Do not infer a count when it is not visible.
- Apply destination on Gupy.
- Company blocklist (config).
- Hybrid or on-site anywhere. Remote only.
- Primary language or runtime outside JavaScript, TypeScript, Node.js, and Go.
  Drop Ruby or Rails, Java-first, Python-first, PHP-first, C# or .NET-first,
  and other outside-primary-stack postings. Do not reject a posting only for
  a framework, library, database, cloud service, or tool.
- Posting knockouts: work authorization the candidate lacks, "not for
  freelancers" with no CLT/EOR path, mandatory location.

Then rank the rest by, in order:

1. **Segment weight** from the config. A direct contract outranks a
   consultancy posting of equal fit.
2. **Seniority match.** Senior first, strong Mid second.
3. **Freshness and competition.** Post age, and comment or applicant count
   where the surface shows it.
4. **Stack overlap** against `~/career/keywords/<segment>.md`.

Drop the rest. Write the drop count and reasons to the ledger head
(**Dropped at triage**) and say them to the user in one line.

### 3. Stream the two waves

Use the approval mode in `~/career/find-me-a-job.md`. Under `auto-advance`,
every posting that passes Maestro triage is approved for tailoring. Under
`user-select`, present the ranked shortlist and stop until the user approves
specific postings.

Wave 1 contains accepted Jobs-tab postings. Start it as soon as Jobs triage
finishes, while the source runner searches Posts. Wave 2 contains accepted Posts-tab
postings. Start it as soon as Posts triage finishes. A wave is a queue, not a
worker batch: every dispatch carries one posting.

Keep the seats pipelined. When the Architect completes one CV, immediately
send that CV to the Analyzer and send the next queued posting to the
Architect. Do not wait for the full wave, the Posts search, or all CVs before
starting a completed CV's review. The source runner, Architect, and Analyzer can run at
the same time, but each seat handles only one posting or surface at a time.

