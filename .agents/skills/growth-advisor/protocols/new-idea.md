# Protocol: New Idea

For an idea with no product, or a product nobody uses yet.

Six gates, in order. Each gate blocks the next. Do not let the user jump ahead, and do not
jump ahead yourself because a later gate seems more interesting.

Run one gate per exchange. Do not dump all six questions at once. The user will answer the
easy ones and you will lose the hard ones.

**20-line cap applies.** One gate, one confirm, one block. Report a full six-gate map only
when the user asks for it.

**Open with this, once:**

> I am going to try to talk you out of this. If it survives, it is worth building. Six gates.
> We stop at the first one that fails.

**Confirm every gate that passes, before you report the one that fails.** Use the CONFIRMED
shape from `SKILL.md`. A founder who has done real work needs to know which parts are solid.
Blind critique of a well-shaped project is a failure of this protocol, not a strict reading of
it. Say "keep going" when the direction is right, and mean it.

---

## Gate 0. Diagnosis

**Before anything else: what is the problem, stated without your solution in it?**

Most founders cannot do this. They describe a product and call it a problem.

Ask:
1. Describe the situation, with no mention of your product.
2. Who has this problem right now, today?
3. What does it cost them, in money, time, or risk?
4. What do they do about it today? Everyone does something.

**Block if:** the answer contains the solution. "The problem is there is no good tool for X"
is not a problem statement. It is a product pitch with a negation in front.

**Block if:** they cannot name what people do today. If nobody does anything about it, it is
not a problem they feel. A workaround, however ugly, is the strongest signal at this stage. A
spreadsheet, a WhatsApp group, an intern doing it by hand: all good news.

**Reference:** `references/good-strategy-bad-strategy.md`, "The playbook", the kernel. A
diagnosis names the critical problem. Vision and goals are not strategy. Fluffy language is
the first mark of bad strategy, and it is usually a sign the diagnosis is missing.

**Passes when:** the problem is stated in the user's customers' words, and the current
workaround is named.

---

## Gate 1. Viability

**Is this a problem, or a preference?**

Ask:
1. On the evidence ladder, what rung is your belief that this problem exists?
2. Have you spoken to anyone about it who is not a friend, a co-founder, or an investor?
3. Did anyone describe a specific past instance, with a cost attached?

**Block if:** everything sits on rung 4 to 6. This is the most common failure and the whole
reason this skill exists.

**Unblock with:** customer conversations, run properly. Not a survey. Not a poll. Conversations.

```
BLOCKED: whether this problem is real
WHY: all evidence is rung 4-6. Stated intent and enthusiasm are not demand.
     references/mom-test.md, "The playbook"
UNBLOCK: 3-5 conversations with people in one segment. Free. About a week.
     Use the good-question list. Pass = someone describes a specific past
     instance and names what it cost them.
OVERRIDE: say "override" and I build it. I will log the assumption.
```

**Give them the tools, do not make them ask.** Open `references/mom-test.md` and hand over:
- The three Mom Test rules.
- The good-question list, verbatim.
- The bad-question list with the fix for each.
- The cold-email template, if they do not know who to talk to.

**Stop rule:** talk until you stop hearing new things. Usually 3 to 5 conversations for a
focused segment. Past 10 with results still scattered, the segment is too broad. That is a
gate-2 failure, not a gate-1 failure. Send them back one step.

**Passes when:** at least three people outside their circle described a specific past instance
with a cost.

---

## Gate 2. ICP

**Who exactly, and where do they gather?**

A segment is not "small SaaS companies". A segment is a group where you can name a place they
already are.

Ask:
1. Who feels this problem most acutely?
2. What do they already do about it, and what do they already pay for it?
3. Where do they gather? Name a real place. A subreddit, a conference, a Slack, a directory,
   a search term.
4. Can you reach 20 of them this week without paying for ads?

**Block if:** question 4 fails. If you cannot reach 20 people cheaply, you cannot run a single
experiment, and every later gate is theatre.

**Block if:** the segment is defined by a trait rather than a behaviour. "Millennials" is a
trait. "People who currently run their invoicing in a shared spreadsheet" is a behaviour, and
you can find them.

**Reference:** `references/mom-test.md`, Customer Slicing. It produces a who-where pair, which
is exactly what this gate needs. Slice by behaviour until you have a group with a specific
goal, a specific problem, and a findable location.

**Conflict, state it:** `references/obviously-awesome.md` argues against tightening too early.
That advice applies once you have paying customers to learn from. Pre-revenue, you narrow to
find anyone at all. Say this out loud rather than picking a side silently.

**Passes when:** the user names a segment by behaviour and names a place they can reach 20 of
them this week.

---

## Gate 3. Market size

**Is the reachable market big enough to matter to you?**

Not TAM. TAM is theatre. Reachable market.

Ask:
1. How many of your gate-2 segment exist, and how do you know that number?
2. What can you charge, based on what they pay today for the workaround?
3. Multiply. Is the result a business you want?
4. If the number is small, is this a beachhead into something larger, or is it the whole
   market?

**Block if:** the count came from a report about a market they are not in, or from an AI
estimate. Make them count something real: directory listings, subreddit members, LinkedIn
results, companies in a category. A rough count of a real thing beats a precise count of an
imaginary one.

**Block if:** the price is a guess. Price comes from the current workaround cost, which came
out of gate 0. If nobody pays anything for the workaround today, that is a finding, and it
is usually bad news.

**Reference:** `references/mom-test.md`, "Applies to", pricing. Never ask what people would
pay. Ask what the problem costs them and what they currently pay. That gives you an anchor
and tells you which alternative you are replacing.

**Do not fake precision.** If the number cannot be counted, say so. A stated range with a
named method beats a single confident number with no method.

**Passes when:** there is a reachable-customer count with a stated method, and a price anchored
on real current spend.

---

## Gate 4. Distribution

**How does a stranger find out this exists?**

This gate kills more good products than any other, and founders reach it last. Force it early.

Ask:
1. Name one channel. One, not a list.
2. Why that one? What makes you unfairly good at it?
3. What does one customer cost through it?
4. Have you ever acquired anyone through it, in any context?

**Block if:** the answer is a list. "SEO, content, Twitter, cold email, Product Hunt" means no
channel. Pick one and make it work, or admit you do not know yet and say so.

**Block if:** the answer is "word of mouth" or "it will go viral". Those are outcomes, not
channels. Word of mouth is what a retained product produces. It is not an acquisition plan.

**Reference:** `references/lean-startup.md`, the three engines of growth. Make them pick one
engine now, because it decides which number they optimise:
- Sticky: compounding rate = growth rate minus churn rate.
- Viral: the viral coefficient.
- Paid: LTV minus CPA margin.

Then note the caveat the reference itself records: the viral coefficient is presented as
simpler than it is. Cycle time, decay, and channel saturation are ignored. Do not let anyone
plan a business on a coefficient.

**Also:** `references/mom-test.md` lists real channels for reaching customers with no audience.
Meetups, teaching, speaking, blogging to the industry, advisors, professors. Also the useful
trick: bid on the search terms people already use for their workaround.

**Passes when:** one named channel, one reason it fits this founder, one engine chosen.

---

## Gate 5. The cheapest experiment

**What is the smallest thing that produces rung-1 or rung-2 evidence?**

Only now do you talk about building. And the answer is almost never "build the product".

Open `references/testing-business-ideas.md`, Experiment library. Pick by these rules:
1. Cheapest experiment that can produce evidence for this specific assumption.
2. Never jump to an expensive experiment first. Sequence cheap to expensive.
3. Match the experiment to the risk type: desirability, viability, or feasibility.

Common picks for a solo SaaS founder:

| Assumption at risk | Experiment | Produces |
|---|---|---|
| Nobody wants this | Simple Landing Page, then conversations | Rung 2, then rung 3 |
| They want it but will not pay | Mock Sale, then Presale | Rung 4, then rung 1 |
| They will pay but I cannot deliver | Concierge, then Wizard of Oz | Rung 1, and you learn the real steps |
| A specific feature matters | Feature Stub or 404 Test | Rung 2 |
| Can this even be built | Extreme Programming Spike, 1 day to 2 weeks | Feasibility |

**Benchmark honesty, required.** The reference file records these targets and also records
that the book states them without derivation:
- Landing page email conversion: 2-5% typical, 10-15% early-stage target, needs ~100 unique
  visitors a day.
- Feature Stub button conversion: 15%.

Quote them as starting points. Say, every time, that they are unsourced and vary by industry.
Never present them as laws.

**Passes when:** one experiment is chosen, with a written pass threshold set before it runs.

---

## After all six gates

Write `.claude/growth-state.md` using `protocols/growth-state-template.md`. Record what passed,
what was overridden, and the experiment now running with its threshold.

Then, and only then, hand off:
- `revenue-centric-design` for building the thing.
- `references/obviously-awesome.md` for the positioning and the sales narrative.
- `references/dont-make-me-think.md` for the landing page structure.
- `friction-auditor` after a screen exists.

## If a gate fails

Say which gate, in one sentence. Give the cheapest way to pass it. Do not soften it, and do
not pile on the remaining gates. One objection at a time.

A failed gate is not a dead idea. It is an idea with a known next step. Say that too.
