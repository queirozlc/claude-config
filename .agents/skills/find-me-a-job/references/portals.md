## Portals

Three dedicated search portals let the runner use two Jobs workers and one
Posts worker in parallel. The surfaces have different URLs, filters, and
result shapes.

| Portal           | Surface                 | Purpose                                                                                                                                             |
| ---------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Jobs Search`    | LinkedIn Jobs tab       | First half of the Jobs query queue.                                                                                                                 |
| `Jobs Search #2` | LinkedIn Jobs tab       | Second half of the Jobs query queue.                                                                                                                |
| `Post Search`    | LinkedIn content search | Recruiter posts. Often no link at all; the recruiter says "talk to me" and gives an email or a WhatsApp number. Highest yield for direct contracts. |
| `Profile Check`  | LinkedIn profile        | One read-only identity snapshot per hunt.                                                                                                           |

### The user creates these, not you

**Do not run `maestri portal create` for them.** A portal made in the Maestri
UI can be given storage **"Shared Globally"**, and a LinkedIn session in such a
portal persists across restarts with no re-login. The CLI has **no storage
option**: `portal create` accepts only URL, name, `--size` and `--simulator`,
and there is no global flag either. Verified 2026-09-01. A CLI-made portal
therefore starts with a cold session and walks straight into the auth wall.

So init **asks the user** to create all four portals in the UI with storage set to
"Shared Globally", then waits for them to appear:

```
maestri list          # confirm both portals are present and named correctly
```

The deterministic source runner drives both and creates neither. Never point a
search portal at the candidate's own profile; profile work belongs to a
different portal.

