## The application

Runs once per approved posting, independently. Several can be in flight on
different seats, but one seat never receives more than one active task.

Order (Lucas, 2026-09-29): **Intake, Posting Analysis, go/no-go, Build,
Verification.** Every decision that the posting alone can answer happens
before the build. No LLM grades the CV after the build.

### 0. Intake (you, the Maestro)

Create the application ledger. Record the posting URL, the exact posting
timestamp and its age, the recruiter's name and profile URL, and any contact
channel given in the post body (email, WhatsApp, a form link). Save the full
posting text verbatim to `~/career/jobs/<slug>.md`. **Never paraphrase a
requirement**; the Analyzer needs the literal tokens.

**Decide the CV language now** and write it to the ledger head. Portuguese
posting from a Brazilian company: `pt`. English posting, or an international
company: `en`. Spanish posting: `es`. One language per posting. Never build
the pair.

**Detect the ATS** from the apply URL with `~/career/ATS-KNOWLEDGE.v2.md`
section 3. Use `generic` when no pattern matches.

### 1. Posting Analysis (Analyzer, before the build)

Dispatch the Analyzer, in the background, with one self-contained prompt:
the posting path, the language, the `ats_profile`, the base path for the
language, and `RUBRIC.md` Part 1. The Analyzer writes:

- `state/<application>-manifest.json`, the spec: `CLAIM` tokens,
  `gap_tokens`, `ask_tokens`, `anchors`, `stack_depth_tokens`,
  `build_instructions`, `projected_required_coverage`, `verdict`.
- `reports/<application>-analysis.md`: eligibility, token table, form pack.

Every Analyzer prompt names an atomic completion sentinel. Dispatch with
`scripts/dispatch_seat.py` ([dispatch](dispatch.md)). Completion requires
both files to exist and the sentinel to verify; the script exit `0` proves it.
The Analyzer never edits a CV and never receives more than one posting.

Routine analysis uses the configured Fable Analyzer. Replace the idle seat
with the Opus command only for one unresolved semantic ambiguity.

### 2. Go / no-go (you, the Maestro)

Read the verdict in the manifest.

- `NO-GO`: abandon. Record the reason in the ledger. No build.
- `ASK`: add the questions to the wave batch for Lucas. After he answers,
  record each gray-zone answer in the DOSSIER whitelist or blacklist, move
  the token in the manifest (`CLAIM` with an anchor, or `GAP`), and
  recompute `projected_required_coverage`. Then decide again.
- `GO`: queue the posting for the Architect.
- `ats_profile: gupy`: no build. Deliver the coverage against the master Gupy
  profile and the form pack.

While the Architect builds posting N, send posting N+1 to the Analyzer.

### 3. Build (Architect)

Dispatch the Architect, in the background, with one self-contained prompt for
**this one posting**: the posting text, the manifest path, the base path for
the chosen language, the voice rule, and the report-back instruction. The
Architect executes the spec. It does not re-decide tokens:

- Every `required_tokens` and `preferred_tokens` entry goes in Skills and in
  one Experience bullet. An anchored token goes in the bullets of its anchor
  role, written as part of that role's domain work.
- Every `stack_depth_tokens` entry goes in Skills.
- Every `build_instructions` entry is applied.
- No token outside the spec is added. No `gap_tokens` entry is written.

The Architect never spawns subagents. It starts from
`~/career/resumes/base-<lang>.tex`, never from scratch. It writes both files
under `~/career/resumes/hunts/<YYYY-MM-DD>/<company-role>/`:
`Lucas-Queiroz-Resume-<lang>.tex` and `Lucas-Queiroz-Resume-<lang>.pdf`.
The role directory identifies the application. The PDF has a professional
upload name. The tailored `.tex` stays next to the PDF.

The Architect never trims Experience. It preserves every verified Experience
role, bullet, and metric from the selected base. It may reword or reorder a
bullet without changing its facts. Prefer one page when the complete content
fits; use two pages when it does not. Spoken-language proficiency goes only in
the separate `Language` or `Idiomas` section: Portuguese Native and English
Fluent (C1).

The Architect copies the base preamble and layout definitions without change.
It does not tune margins, spacing, font size, or role macros.

Recruiter readability is a build rule (`CV-SPEC.md`): target title near the
top, the three most relevant bullets first in the most recent role,
past-tense XYZ bullets, at least 3 real numbers, no buzzwords, grouped Skills.

Every Architect prompt names an atomic completion sentinel. After all required
files exist and are non-empty, the Architect runs `scripts/worker_sentinel.py
write`. Dispatch with `scripts/dispatch_seat.py`. Completion requires the
sentinel to verify; the script exit `0` proves it. Run the gate in the turn
that the script's exit starts. A fix round is a new dispatch with a new task
ID and a new sentinel path.

Maintain `~/career/resumes/hunts/<YYYY-MM-DD>/README.md` as the hunt resume
index. One row maps company, exact role, exact job link, PDF link, and
application status. Use the LinkedIn job URL when it exists. For a post without
a permalink, use the observed external apply link. Every application ledger
and final hunt summary uses the same link and exact PDF path.
Never move or edit the base CVs or prior files under `resumes/archive/` while
organizing a current hunt.

### 4. Verification (script)

At the start of the hunt, cache the LinkedIn profile once:

```
python3 scripts/cache_linkedin_identity.py \
  --portal "Profile Check" \
  --output state/<hunt-id>-linkedin-identity.json
```

All applications in the hunt use this cache.

Run `scripts/resume_gate.py` on the built CV (`RUBRIC.md` Part 2). It checks
extraction, sections, contact, layout, roles, LinkedIn identity, Experience
completeness, forbidden terms, the claim allowlist, required-token placement,
the spec anchors and stack depth, the blacklist, GAP tokens, and required
coverage.

- Exit `0`: the package is ready. Go to delivery.
- Exit `1`: send the failure list from the gate report to the Architect.
  Run the gate again. Two rounds maximum, then escalate to Lucas.
- Exit `2`: the gate could not run. Fix the input and run it again.
