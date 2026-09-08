## Init flow (`/find-me-a-job init`, `/find-me-a-job start`, or auto-triggered when no config exists)

Init is not a config writer. It is **interview, recruit, start**. It ends with
the hunt running, never with a file and a shrug.

1. **Detect** everything detectable (below). Never ask what you can read.
2. **Interview** the user with the AskUserQuestion tool for what detection
   cannot resolve. Give every question a recommended option and say why.
   Always confirm the seat roster: **which seats, which roles, and which
   harness each one runs.** Never assume a seat's model; the wrong harness on
   the wrong seat is the main cost mistake in a hunt.
3. **Write the config** to `~/career/find-me-a-job.md`.
4. **Recruit** the approved seats and verify the user-created portals.
5. **Start the hunt.** Do not stop after init. Init that ends without a
   running hunt has not finished.

Never re-detect on normal runs; the config is the cache.

**Detect:**

- **Seats:** run `maestri list`. **Every active seat starts fresh.** If the seat
  already exists on the canvas, swap it in place with `--replace` (see [Harnesses](team.md)); if
  not, recruit it with `--role` and the config's launch command. Record the
  exact agent names in the config. `maestri role list` may show a role "in
  use" by a terminal that is not on this canvas. That is stale; ignore it.
  Do not recruit or replace the Market Scout unless the source runner reports
  a parser failure.
- **Existing roles:** `maestri role list`. `Market Scout`, `Resume Architect`
  and `ATS Analyzer` are global roles; reuse them, do not recreate them.
- **Portals:** `maestri list` shows connected portals. A hunt needs three
  dedicated search portals: `Jobs Search`, `Jobs Search #2`, and
  `Post Search`. It also needs the read-only `Profile Check` portal. Never
  reuse a search portal for profile work.
- **Dossier state:** check the identity fields, LinkedIn titles and dates,
  career history, and match-weight policy. Report missing required fields.
- **Existing corpora:** list `~/career/keywords/`. A segment with no corpus
  needs a sourcing run before any application can tailor against it.

**Ask the user** only what detection cannot resolve: which harness preset for
each seat, the segment weighting if it has changed, the shortlist size per
hunt, and the reset command per seat's harness.

**Write the config** using this template:

```markdown
# find-me-a-job config

## Candidate

- Dossier: ~/career/DOSSIER.md
- Knowledge base: ~/career/ATS-KNOWLEDGE.md
- Rubric: ~/career/RUBRIC.md
- CV spec: ~/career/CV-SPEC.md
- Base CV: ~/career/resumes/base-en.tex and base-pt.tex

## Segments, in weight order

1. <segment key> — <description>
2. ...

Seniority target: <e.g. Senior preferred, strong Mid acceptable>

## Sourcing

- Recency cut: <e.g. past 24h first, past week widest>
- Surfaces: jobs-tab, posts, both every hunt, in parallel
- Shortlist size per hunt: <N>
- Query template: <e.g. (<stack alternates>) AND <seniority> AND <region>>
- Triage knockouts: <destinations, company blocklist, hybrid/on-site, primary language or runtime>

## Portals

| Portal name | Surface | Owned by |
| ----------- | ------- | -------- |
| ...         | ...     | ...      |

## Seats

| Seat | Agent name | Role | When | Preset | Reset cmd |
| ---- | ---------- | ---- | ---- | ------ | --------- |
| ...  | ...        | ...  | ...  | ...    | ...       |

## Review checks

- Hard: the File Readability Check, Role Eligibility Check, and required part
  of the Resume Evidence Check must fully PASS. Every required token must
  appear in `Skills` and in one relevant `Experience` bullet.
- Reported, not blocking: preferred-token coverage in the Resume Evidence
  Check and the Recruiter Readability Score.
- Every blocked result must quote the exact posting requirement, list the
  evidence checked and found, explain why it failed, classify the fix as
  `CV FIX`, `LUCAS CONFIRMATION`, or `ROLE MISMATCH`, and give one next action.

## Delivery shape

- One posting per Architect dispatch. No fan-out.
- One language per tailored CV, decided by Maestro at intake.
- CV voice per CV-SPEC.md.

## Notes

<language rules, contract types available, misc conventions>
```

