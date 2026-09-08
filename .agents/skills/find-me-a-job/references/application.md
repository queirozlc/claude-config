## The application

Runs once per approved posting, independently. Several can be in flight on
different seats, but one seat never receives more than one active task.

### 0. Intake

Create the application ledger. Record the posting URL, the exact posting
timestamp and its age, the recruiter's name and profile URL, and any contact
channel given in the post body (email, WhatsApp, a form link). Save the full
posting text verbatim to `~/career/jobs/<slug>.md`. **Never paraphrase a
requirement**; the Analyzer needs the literal tokens.

**Decide the CV language now** and write it to the ledger head. Portuguese
posting from a Brazilian company: `pt`. English posting, or an international
company: `en`. Spanish posting: `es`. One language per posting. Never build
the pair.

Write `state/<application>-manifest.json` with `application_id`, `language`,
`required_tokens`, and `preferred_tokens`. This is the deterministic gate
input. Do not add a token that the posting does not state.

### 1. Context pass (you, the Maestro)

Extract, from the posting's own words: required versus preferred skills, the
knockouts (work authorization, location, time-zone overlap, English level,
years of experience), the contract shape, and the seniority label. Where the
posting is silent, write `not stated`. Never infer a requirement.

Classify every technical token with the dossier's match weights:

1. Primary language or runtime, weight 4.
2. Framework or library, weight 3.
3. Data, messaging, cloud, or tool, weight 2.
4. Practice or adjacent term, weight 1.

The brief states `Primary language or runtime:`, `Exact required match
tokens:`, and `Preferred match tokens:`. An accepted posting must use
JavaScript, TypeScript, Node.js, or Go as its primary stack.

This brief travels with every prompt you send.

### 2. Tailor

Dispatch the Architect, in the background, with one self-contained prompt for
**this one posting**: the posting text, your brief, the base path for the
chosen language, the segment's keyword corpus, the voice rule, and the
report-back instruction. Several postings mean several dispatches, one after
another as the seat goes idle, each with its own `.out` file and its own log
line. The Architect never spawns subagents.

As soon as one Architect dispatch completes, send that CV to the Analyzer.
Then send the next queued posting to the Architect without waiting for the
Analyzer or for the other sourcing surface.

The Architect starts from `~/career/resumes/base-<lang>.tex`, never from
scratch. It writes both files under
`~/career/resumes/hunts/<YYYY-MM-DD>/<company-role>/`:
`Lucas-Queiroz-Resume-<lang>.tex` and `Lucas-Queiroz-Resume-<lang>.pdf`.
The role directory identifies the application. The PDF has a professional
upload name. The tailored `.tex` stays next to the PDF; the Analyzer and the
user need the source.

The Architect never trims Experience. It preserves every verified Experience
role, bullet, and metric from the selected base. It may reword or reorder a
bullet without changing its facts. It must not delete content to save space or
improve match. Prefer one page when the complete content fits; use two pages
when it does not. Spoken-language proficiency goes only in the separate
`Language` or `Idiomas` section: Portuguese Native and English Fluent (C1).

The Architect copies the base preamble and layout definitions without change
on the first draft. It does not tune margins, spacing, font size, or role
macros. The approved base layout is the default. A complete two-page CV is
valid when the unchanged layout does not fit on one page.

Every Architect prompt names an atomic completion sentinel. After all required
files exist and are non-empty, the Architect runs `scripts/worker_sentinel.py
write`. The terminal reply is secondary evidence. Completion requires the
exec session to exit and the sentinel to verify.

Maintain `~/career/resumes/hunts/<YYYY-MM-DD>/README.md` as the hunt resume
index. One row maps company, exact role, exact job link, PDF link, and
application status. Use the LinkedIn job URL when it exists. For a post without
a permalink, use the observed external apply link. Every application ledger
and final hunt summary uses the same link and exact PDF path.
Never move or edit the base CVs or prior files under `resumes/archive/` while
organizing a current hunt.

### 3. Review

At the start of the hunt, cache the LinkedIn profile once:

```
python3 scripts/cache_linkedin_identity.py \
  --portal "Profile Check" \
  --output state/<hunt-id>-linkedin-identity.json
```

All applications in the hunt use this cache. Do not open the profile portal
again for each CV.

Before Analyzer dispatch, run `scripts/resume_gate.py`. It checks PDF
extraction, contact and section fields, LinkedIn identity fields, exact base
roles, Experience bullet and metric completeness, forbidden terms, required
token placement, the approved base layout, and `claim-allowlist.json`. It
writes a deterministic report, a reduced review packet, and a completion or
blocked sentinel.

Dispatch the Analyzer, in the background, with the generated review packet.
The packet contains the posting, CV delta, claim manifest, and deterministic
gate report. The Analyzer grades semantic truth, Role Eligibility, and
Recruiter Readability. It opens the full CV only when the packet identifies an
ambiguity. It does not repeat deterministic checks that passed.

Routine review uses the configured Fable Analyzer. If it identifies one
unresolved semantic ambiguity after it reads the dossier evidence, replace
the same idle seat with the configured Opus command and dispatch only that
ambiguity. Do not start Opus for a routine pass.

Every Analyzer prompt names an atomic completion sentinel and complete report
path. Completion requires the exec session to exit, the report to exist, and
the sentinel to verify. The terminal reply is secondary evidence.

Review each completed CV immediately. Do not wait for all CVs in the wave. The
Analyzer handles one CV per dispatch and never receives a multi-posting batch.

**Blocking checks.** The File Readability Check and Role Eligibility Check must
fully PASS. The Resume Evidence Check must place every required posting token
in `Skills` and in one relevant `Experience` bullet. Any failed blocking check
means the package does not go out. Send `CV FIX` defects to the Architect and
review the result again. Ask Lucas about `LUCAS CONFIRMATION` items. Abandon a
`ROLE MISMATCH`.

**Required decision explanation.** A blocked result is incomplete unless it
contains a Decision Explanation table with one root cause per row. Each row
must include the check name, exact posting text, evidence checked, evidence
found, direct failure reason, fix type, and next action. If one fact affects
both Role Eligibility and Resume Evidence, list it once as the root cause and
cross-reference it in the token table.

**Reported, not blocking.** Preferred-token coverage in the Resume Evidence
Check and the Recruiter Readability Score travel with the package.

Two fix rounds maximum on Recruiter Readability style points. Do not ping-pong wording
forever.

Never let the Architect grade its own fix. The Analyzer re-runs it.

