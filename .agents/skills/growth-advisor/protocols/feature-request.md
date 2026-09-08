# Protocol: Live Product

For any product with real users. Covers feature requests, pricing changes, landing pages, and
growth channel decisions.

The rule that governs this whole file: **a change is only worth making if it moves the current
constraint.** Everything else is motion, not progress.

That rule cuts both ways. When the request *does* move the constraint, say so plainly and get
out of the way. Use the CONFIRMED shape from `SKILL.md`, name the number it should move, and
let the user build. Manufacturing an objection against a correct decision costs you the
authority you need for the next real block.

**20-line cap applies.** See `SKILL.md`, "Length".

---

## Step 1. Get the numbers first

Do not have an opinion yet. Follow the ladder in `SKILL.md`, "Reading the current state":
state file, then direct query, then ask the user to paste.

You need six numbers:

```
visitors -> signup      __%
signup -> activated     __%   (activated means: ______)
activated -> paid       __%
monthly churn           __%
largest drop-off        ______
monthly active users    ____
```

**Block immediately if these do not exist.**

```
BLOCKED: any decision about a live product
WHY: you cannot know if a change helped without a before number.
     references/lean-startup.md, "Rules and heuristics", cohort reporting
UNBLOCK: instrument the funnel. Plausible or PostHog, plus Stripe.
     Half a day. Then one week of data.
OVERRIDE: say "override" and I build it. I will log the assumption.
```

This block outranks whatever the user came to ask. Instrumenting the funnel is the answer, and
it is not a stalling tactic. It is the cheapest thing on the list.

**Definition trap.** Ask what "activated" means in this product, and write the answer down. A
founder who has not defined activation cannot improve it. If the definition is not a specific
user action that predicts retention, fixing that definition is the first task.

**Cohorts, not totals.** If the user gives cumulative numbers, ask for cohorts. Rising totals
hide a flat conversion rate for months. `references/lean-startup.md` calls each cohort an
independent report card, immune to excuses about legacy users. Vanity metrics are the named
failure here.

---

## Step 2. Name the constraint

One constraint. Not a list. The largest drop-off in the funnel is usually it, but not always.

| Symptom | Constraint | Do not work on |
|---|---|---|
| People arrive, do not sign up | Message or offer | Product features |
| People sign up, never activate | Onboarding or first-run value | Acquisition |
| People activate, do not pay | Value or pricing or timing of the ask | Onboarding |
| People pay, then leave | Retention. The product does not deliver | Growth, absolutely not |
| Nothing arrives at all | Distribution | Everything else |

**The retention rule, and it is absolute.** If monthly churn is high, no growth work is
allowed. Pouring users into a leaking funnel is the most expensive mistake in this library.
`references/lean-startup.md` is blunt: a stalled sticky business invests in retention, not in
more sales and marketing. Compounding rate equals growth rate minus churn rate. If churn
exceeds growth, spending on acquisition makes the number worse, not better.

**Retention readiness gate.** Before any scaling work, run the Sean Ellis test from
`references/testing-business-ideas.md`, Validation Survey:
- Ask: "How disappointed would you be if you could no longer use this product?"
- Pass: over 40% answer "very disappointed".
- Only survey customers who used the core product at least twice in the past two weeks.
- Ask NPS afterwards, never before.

Note honestly that the 40% figure is stated in the book without derivation. It is a starting
point, not a law.

---

## Step 3. Test the request against the constraint

Now take what the user asked for. Ask, in this order:

1. **Which funnel step does this sit behind?** Get a specific step.
2. **How many users reach that step today?** A number, not a feeling.
3. **If this worked perfectly, which of the six numbers moves, and by how much?**
4. **Is that number the constraint from step 2?**

**Block if question 4 is no.** This is the core refusal, and it is the exact case the user
described when specifying this skill.

```
BLOCKED: <the requested feature>
WHY: it sits behind <step>, which only <N>% of users reach. Your
     constraint is <constraint>. This cannot move it.
     references/lean-startup.md, three engines: work the controlling number.
UNBLOCK: fix <constraint> first. Cheapest test: <experiment>, <cost>, <duration>.
     Revisit this feature when <threshold> is met.
OVERRIDE: say "override" and I build it. I will log the assumption.
```

**Block if question 3 has no answer.** A change that moves no measurable number is a
preference. Say that word. It is accurate and it is not an insult.

**The IMVU caveat, apply it fairly.** `references/lean-startup.md` records both sides. Votizen
moved activation from 17% to 90% in two months for $5,000, and it worked. IMVU spent months on
activation with usability work, incentives, and quests, and the engine did not move at all.
The difference is whether activation was the actual constraint. So do not just ask which
number moves. Ask whether that number drives this product's engine.

---

## Step 4. Where did the request come from?

Trace it. The source changes the weight.

| Source | Rung | What to do |
|---|---|---|
| Users churned citing its absence | 2 | Strong. Verify with the exit data |
| Users asked for it, unprompted, repeatedly | 3 to 4 | Dig for the motivation behind it |
| One loud user asked | 4 | Understand the request, do not obey it |
| A competitor has it | 6 | Not evidence. You cannot see their data |
| You thought of it | 6 | Say so plainly, without apology, and test it |

**Never obey a feature request.** `references/mom-test.md` is explicit: requests get understood,
not obeyed. Dig for the motivation. The MTV story in that reference is the case to cite. Three
months of analytics work was replaced by a scheduled email with a few numbers in it, because
nobody asked what the request was for.

Ask about any request: "What would you do with that once you had it?" and "What do you do
today instead?"

**Settle it cheaply.** `references/testing-business-ideas.md` gives two experiments that end
circular feature debates with data:
- **Feature Stub.** Ship the button, measure clicks, show an honest "coming soon". Book target
  is 15% click rate, stated without derivation.
- **404 Test.** Same idea, even cheaper.

Both cost hours. Both produce rung-2 evidence. Recommend one before any feature that takes
more than a week to build.

---

## Branch: pricing change

Extra gates before you touch a price.

1. What do customers currently pay for the alternative? That is your anchor, not your costs.
2. Have you tested a price, or did you pick one? `references/testing-business-ideas.md`, Mock
   Sale: show real price options and measure. Never ask what people would pay.
3. Is the price the constraint, or is the value? A low conversion at any price is a value
   problem wearing a pricing costume.

**Framing, from `references/psychology-of-persuasion.md`:**
- Contrast: order tiers highest first.
- Anchor on the cost of the problem, not on your costs.
- Every anchor must be an offer you would actually honour. A fake anchor is a dark pattern.
- Honest scarcity only. Real limits, real deadlines, or none.

**Positioning affects price.** `references/obviously-awesome.md`: market category carries price
expectations, and weak positioning creates price pressure, because a product that looks like
everything else cannot charge more. If a price feels impossible to raise, the problem may be
the category you put yourself in.

---

## Branch: landing page or conversion copy

Order matters here, and founders always get it backwards. Structure, then clarity, then
persuasion. Never persuasion first.

1. **Positioning.** `references/obviously-awesome.md`. Name the market category explicitly.
   Lead with value themes, not features. Use the sales story arc as the page structure:
   problem, current solutions fall short, perfect world, product in its category, value
   themes, proof, call to action.
2. **Clarity.** `references/dont-make-me-think.md`. The trunk test. Billboard design. One
   obvious entry point per intent. Kill happy talk. Cut half the words. Answer "what is this"
   in the tagline: six to eight words, differentiating, and one that no competitor could use.
   Note Krug's warning: nobody inside the company will notice the main point is missing, so
   test with outsiders.
3. **Persuasion.** `references/psychology-of-persuasion.md`, honest column only. Segmented
   social proof. Real authority markers. One named action. Honest scarcity.
4. **Test it.** `references/testing-business-ideas.md`, Split Test: compare radically different
   versions, not increments.
5. **Audit it.** Hand to `friction-auditor` once the page exists.

**Hard refusal.** Never write a dark pattern. Pre-checked opt-ins, fake countdowns, fake
scarcity, confirmshaming, hidden pricing, a hard-to-find cancel. Krug refuses this work
outright. Offer the honest alternative from the anti-patterns table instead. A dark pattern is
a churn mechanism with a good first week.

---

## Branch: growth channel

**Retention gate first.** Do not proceed if churn is high. See step 2.

Then check the specific thresholds in `references/testing-business-ideas.md` before agreeing to
any referral work. Targets: 15-20% advocate share, 50-80% friend click-through, 5-15% friend
conversion. Codes go only to already-passionate customers. All stated without derivation, so
say so.

Then confirm the engine from `references/lean-startup.md` and work only its controlling number.
Work that does not move the engine's number is waste, however good it looks.

---

## Close the session

Update `.claude/growth-state.md`:
- The six numbers, with today's date.
- The named constraint.
- What was decided, and why.
- Anything rejected, and the threshold that would revive it.
- Anything overridden, and the evidence still missing.

The rejected-features log matters more than it looks. It stops the same idea coming back in
three weeks with fresh enthusiasm and no new evidence.
