# Template: growth-state.md

Copy this into `<project>/.claude/growth-state.md`. The advisor reads it first and updates it
at the end of every session.

Keep it short. A state file nobody updates is worse than none, because it lies with authority.
Every number carries a date and a source. Delete a number rather than let it go stale.

```markdown
# Growth State

Last updated: YYYY-MM-DD

## Product
One sentence. What it does, for whom.

## ICP
Segment, defined by behaviour, not by trait.
Where they gather: <a real, named place>
Can I reach 20 this week without ads: yes / no

## Positioning
Market category: <the category you compete in>
Value themes: <2-3, in customer words>
Best-fit customer looks like: <observable traits>

## Funnel
| Step | Rate | As of | Source |
|---|---|---|---|
| visitors -> signup | % | YYYY-MM-DD | |
| signup -> activated | % | YYYY-MM-DD | |
| activated -> paid | % | YYYY-MM-DD | |
| monthly churn | % | YYYY-MM-DD | |

Activated means: <a specific user action that predicts retention>
Monthly active users: <number>

## Current constraint
<One. Not a list.>
Evidence: <which number says so>

## Engine
Sticky / viral / paid. Pick one.
Controlling number: <compounding rate | viral coefficient | LTV-CPA margin>
Current value: <number, or "not measured">

## Retention gate
Sean Ellis test: __% very disappointed, as of YYYY-MM-DD
Gate is 40%. Scaling work is blocked until it passes.

## Running experiments
| Experiment | Assumption tested | Pass threshold | Started | Result |
|---|---|---|---|---|

Set the threshold before the experiment runs. A threshold written afterwards is a story.

## Rejected features
| Feature | Rejected on | Why | Revive when |
|---|---|---|---|

## Overridden assumptions
| Date | Decision | Evidence still missing |
|---|---|---|

Review this table monthly. Overrides are debt. This is where the next failure is written down
before it happens.

## Customer evidence
Verbatim quotes only, with a date and a source. Never paraphrase into this section.
Rung 1-3 evidence only. Compliments do not belong here.
```
