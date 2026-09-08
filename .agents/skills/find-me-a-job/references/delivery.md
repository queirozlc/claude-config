### 4. Package

Render the approved CV to PDF, then **verify the extraction before you call it
done**:

```
pdftotext resume.pdf - | head -40
```

Confirm the contact block, the section headers, and every employment block
survive. A PDF nobody extracted is a PDF nobody has tested.

### 5. Deliver

Write one Maestri note per position and notify the user. This is the terminal
agent action. **Agents never submit an application.** No portal clicks a
submit button, no form is filled on the candidate's behalf, no message is sent
to a recruiter. The user applies.

Note name: `apply-<company>-<role-slug>`. File it into a fichário so the
canvas stays organized: `maestri note create ... --stack "Applications"`.

The note carries exactly this:

```markdown
# Apply — <Company> — <Role>

**Segment:** <us-direct | br-pj | agency> **Fit:** <one line>
**Posted:** <YYYY-MM-DD HH:MM> (<age> old) **Competition:** <N comments, or n/a>

## Where to apply

<application URL>
<or: "No link. Contact the recruiter directly.">

## Which CV to send

`<absolute path to the PDF>`
File Readability PASS · Role Eligibility PASS · Resume Evidence PASS (<NN>/100) · Recruiter Readability <NN>/100

## Recruiter

<Name> — <profile URL>
Contact: <email / WhatsApp / "LinkedIn DM only">

## Message to send

<the full message, ready to paste, in the posting's language>

## Screening answers, prepared

- Time-zone overlap: <the exact answer>
- English level: <the exact answer>
- Contract type: <PJ / CLT / contractor>
- Years of experience: <answer>
- Notice period: <answer>
- <any other question the posting asks, with its answer>

## Match limits

<preferred tokens not placed, or "None">

## Deadline

Apply within <N> hours. This posting was <age> old at intake and the
competition proxy was <N>.
```

The **Message to send** is written by the Architect, not by you, and it obeys
the posting's language. Many LatAm recruiter posts are in Spanish or
Portuguese. A Portuguese post gets a Portuguese message.

Then: `maestri notify "<Company> <Role> is ready. See note apply-<slug>."`

Set Phase to `5-delivered`.

### 6. Close

When the user confirms they applied, set Phase to `6-applied`, append the log
line, and keep the ledger until the user says to delete it. It is the record
of which CV went where, which is the input to any future follow-up loop.

If the user abandons the posting, set Phase to `abandoned` with a one-line
reason and stop.

## Hunt summary note (mandatory at the end of every hunt)

Requested by Lucas, 2026-09-02. When every application in the hunt has
reached `5-delivered` or `abandoned`, write one Maestri note named
`hunt-<YYYY-MM-DD>-summary`, filed with `--stack "Hunts"`, and notify.
Lucas reads this one note to apply to everything. It carries:

```markdown
# Hunt <YYYY-MM-DD> — summary

Found <N> · dropped <N> at triage · approved <N> · delivered <N> · abandoned <N>

| #   | Company · Role                      | Segment   | Lang | Primary stack      | Resume                | Blocking checks | Resume Evidence | Recruiter Readability | Recruiter · channel      | Apply within |
| --- | ----------------------------------- | --------- | ---- | ------------------ | --------------------- | --------------- | --------------- | --------------------- | ------------------------ | ------------ |
| 1   | [<Company> — <Role>](<posting url>) | us-direct | en   | TypeScript/Node.js | `<absolute PDF path>` | PASS/PASS/PASS  | 94              | 81                    | <Name> · <email/DM/form> | <N> h        |

## Cold messages

### <Company> — <Role>

Send to: <channel>
<the full message, ready to paste, in the posting's language>

## Match limits

- <Company>: <preferred token not placed, or none>

## Abandoned

- <Company> — <Role>: <one-line reason>
```

Every value comes from the application ledgers, the review reports, and the
message files. Never write a score that is not in a Sieve review report.
The per-application `apply-<slug>` notes stay; the summary links nothing
new, it collects.

