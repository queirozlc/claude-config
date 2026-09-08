# The Lean Startup — Eric Ries

> A management method for deciding what to build when you do not yet know who your customer is or what they will pay for.

## When to reach for this

- You have an idea and no paying customers. You must decide what to build first.
- Your product ships often, your gross numbers rise, and you cannot tell if any change caused the rise.
- Growth has flatlined and you do not know whether to add features, cut price, or buy ads.
- You are about to commit months of build time to a plan based on assumptions nobody tested.
- You suspect the current strategy is wrong but you cannot prove it, so you keep optimizing.

## Core thesis

- A startup is "a human institution designed to create a new product or service under conditions of extreme uncertainty." Uncertainty is the defining condition, not size or sector.
- The unit of progress is validated learning, not shipped features. Learning is validated only by measured changes in customer behavior.
- Any work not required to learn what customers want is waste. This includes good code, good design, and good process.
- Build-Measure-Learn is the core loop. You plan in reverse: decide what to learn, then what to measure, then what to build.
- Two assumptions carry the whole plan: the value hypothesis (do users get value once they use it) and the growth hypothesis (how new users arrive). Test these first.
- Customers cannot tell you what to build. Run experiments on them instead of asking them.
- Vanity metrics (totals, cumulative counts) hide the truth. Actionable, cohort-based metrics reveal it.
- Growth comes from one of three engines: sticky, viral, paid. Pick one. Its metrics tell you what to work on.
- A pivot is a structured change of strategy to test a new fundamental hypothesis. Runway is the number of pivots you can still make.
- Speed is the only durable advantage. "The only way to win is to learn faster than anyone else."

## The playbook

### 1. Write down the leap-of-faith assumptions

1. Write the business plan as a list of assumptions, in the present tense, with a straight face. Example: "We assume 10 percent of customers who see the free trial offer will sign up."
2. Separate mundane assumptions (well-established industry facts) from leaps of faith (if false, the venture fails).
3. Kill argument-by-analogy. Rewrite every analogy in its full form and check each factual claim:
   - Bad form: "Previous technology X won market Y because of attribute Z. Our X2 has Z, so we win Y2."
   - Good form: state that large numbers of people already want this, know they want it, can afford it, and are blocked only by the specific thing you fix. Then test that.
4. Use Komisar's analogs and antilogs. An analog is a prior product that already answered a question for you (Walkman answered "will people listen to music in public with earphones?"). An antilog is a prior product that proved the opposite (Napster proved people would not pay for downloaded music). What is left over, after analogs and antilogs, are your leaps of faith.
5. Always list at least these two:
   - **Value hypothesis**: do customers get real value once using it?
   - **Growth hypothesis**: how do new customers find it?

### 2. Get out of the building

1. Talk to potential customers before you design a solution. Scott Cook validated Intuit by calling names at random from two phone books, asking only: do people find it frustrating to pay bills by hand?
2. Ask about the problem, not about proposed features. Early conversations exist to confirm the problem is worth solving.
3. Practice genchi gembutsu: go and see for yourself. Do not accept the reports of others.
4. Write a customer archetype: a brief document that humanizes the target customer and guides daily prioritization. Treat it as a hypothesis, provisional until validated.
5. Run Mark Cook's (Kodak Gallery) four questions in order. Most teams skip to question 4:
   1. Do consumers recognize that they have the problem you are trying to solve?
   2. If there was a solution, would they buy it?
   3. Would they buy it from us?
   4. Can we build a solution for that problem?
6. Avoid both failure modes: "just do it" (build after a few cursory conversations) and analysis paralysis (endless refining at the whiteboard). Neither detects errors, because errors live in the interaction between product and customer.

### 3. Build the minimum viable product

Definition: the version of the product that enables a full turn of the Build-Measure-Learn loop with the minimum amount of effort and the least development time. It is not necessarily the smallest product imaginable.

Rule: remove any feature, process, or effort that does not contribute directly to the learning you seek.

Rule: when in doubt, simplify. Most founders overestimate how many features an MVP needs.

Sell to early adopters first. They accept an 80 percent solution and fill in the gaps with imagination. Polish beyond what early adopters demand is waste.

**MVP patterns, with their source cases:**

| Pattern | What it is | Case |
|---|---|---|
| Smoke test | Offer a preorder for a product that does not exist. Measures one thing: are customers interested enough to try. | Direct-marketing technique; recommended before building a prototype |
| Video MVP | A short demo of the product working as intended, aimed at a specific early-adopter community | Dropbox. Beta waiting list went from 5,000 to 75,000 people overnight |
| Concierge MVP | Deliver the service by hand, in person, to one customer at a time. Charge money. | Food on the Table. First customer got weekly in-person visits from the CEO and VP of product, and paid $9.95 per week |
| Wizard of Oz | Customers believe they use the product; humans do the work behind the scenes | Aardvark ran 8 people manually managing queries for nine months, through seed and Series A |
| Manual-first commerce | Do the transaction by hand before building any system | Zappos photographed shoes in local stores and bought them at full price when a customer ordered |
| Cobbled-together stack | Use off-the-shelf tools with no custom code | Groupon: a skinned WordPress blog, FileMaker-generated coupon PDFs, e-mailed with Apple Mail |
| Existing-tool MVP | Deliver your new method through a tool that already exists | Grockit taught test prep over WebEx and reached $10,000 to $15,000 per month with no custom software |

**Iteration rhythm from Aardvark**: six prototypes, each a two- to four-week effort, each shown to 100-200 friends, measured by how many came back. Results were unambiguously negative until the sixth.

**Before you ship the MVP**, commit in advance that you will not give up hope whatever the result. MVPs usually produce bad news.

**Handle the four common objections:**

- *Patents*: in some jurisdictions release starts the filing clock. Get legal counsel. In most industries the learning benefit outweighs the risk.
- *Competitors stealing the idea*: try to get an established company to steal one of your lesser ideas. You will fail. Managers are already drowning in good ideas. If a competitor can outexecute you once they know the idea, you were doomed anyway.
- *Brand damage*: launch the MVP under a different brand name. Reputational damage comes from loud PR that the product fails to match, not from being obscure. Do the public marketing launch after the product proves itself.
- *Morale*: agree ahead of time that the MVP is step one, not a go/kill gate.

### 4. Set up innovation accounting

Three steps, repeated:

1. **Establish the baseline.** Use an MVP to get real numbers into your growth model: conversion rates, sign-up and trial rates, customer lifetime value. Test the riskiest assumption first. If you cannot move that one, testing the others is pointless.
2. **Tune the engine.** Every product, marketing, or design initiative must target one driver of the growth model. If a design change does not improve the metric it targeted, judge it a failure. "A good design is one that changes customer behavior for the better."
3. **Pivot or persevere.** If the numbers are converging toward the plan's ideal, continue. If the ideal keeps receding, pivot and re-establish a new baseline.

**Buy a small, constant flow of new users to measure against.** IMVU spent $5 per day on Google AdWords. At a 5-cent minimum bid, that bought 100 clicks per day: not significant marketing, but a fresh report card every single day.

**Use cohort analysis, never cumulative totals.** Group users by the period they arrived. For each cohort, report the percentage that took each action in your funnel. IMVU tracked: registration, download, trial, repeat usage, purchase. Their cumulative graph looked like a hockey stick. Their cohort graph showed repeat usage rising from under 5 percent to almost 20 percent while purchase stayed stuck near 1 percent for seven months. Only the cohort view showed the strategy was broken.

**Split-test every feature.** Offer different versions to different users at the same time and compare behavior. Many features that engineers and designers consider improvements have zero impact on behavior. Split testing costs extra accounting and saves far more time by eliminating work that does not matter. Grockit split-tested "lazy registration," an accepted industry best practice that cost them significant ongoing support: forced registration produced exactly the same registration, activation, and retention rates. The extra effort was pure waste, and the result revealed something bigger: customers were deciding based on marketing and positioning, not on product experience.

**The three A's of a metric:**

- **Actionable**: it shows clear cause and effect. If you cannot say what action would replicate the result, it is a vanity metric. "Hits" fails this test.
- **Accessible**: reports use people-based units that everyone understands, and everyone can see them. Grockit e-mailed every employee a daily document with the results of every split test in plain English. IMVU made reports part of the product, on the website, one page per experiment, viewable by any employee.
- **Auditable**: you can spot-check the data by talking to real customers. Draw reports directly from master data, not an intermediate system. When data is overturned by a technical fault, team confidence and discipline collapse.

**Vanity metrics to refuse**: total registered users, total revenue, hits, total questions answered, cumulative anything. They rise when the engine is merely turning, which hides the fact that your work is having no effect.

### 5. Run product work as a pull system

1. Plan in reverse: decide what to learn, then what to measure, then what to build. The hypothesis pulls work from product development. Any other work is waste.
2. Work in small batches. Single-piece flow beats large batches even when each step takes the same time, because defects surface immediately and rework disappears.
3. Use a kanban board with four states and a hard cap (IMVU/Grockit used a cap of three per bucket):
   - backlog
   - being built
   - done (feature-complete technically)
   - being validated
4. Define "validated" as: knowing whether the story was a good idea to have been done in the first place. Usually a split test; sometimes interviews or surveys.
5. A story leaves the board only when validated. If validation fails, remove the feature from the product.
6. Expect the board to jam at first. The only way to unblock it is non-engineering work: talking to customers, reading split-test data. That is the point.
7. Build an immune system. Automated checks should detect business consequences, not only functional correctness (a checkout button turned white-on-white passes functional tests and kills the business). On detection: revert the change automatically, notify the team, block further changes, and do not unblock until root cause is fixed.
8. Beware the large-batch death spiral. Batches grow because moving a batch forward creates rework and interruption, so everyone wants bigger batches. There is no physical limit on batch size in software. Eventually one release becomes a bet-the-company event nobody dares ship.

### 6. Decide: pivot or persevere

**Schedule the meeting in advance.** Less than a few weeks between meetings is too often; more than a few months is too infrequent. Find your own pace.

**Who attends**: product development leadership and business leadership. Add outside advisers who can see past your preconceptions.

**What each side brings**:
- Product development: a complete report of optimization results over time, not just the last period, compared against expectations over time.
- Business leadership: detailed accounts of conversations with current and potential customers.

**Symptoms that you should pivot**:
- Product experiments are becoming less effective.
- The general feeling that product development should be more productive.
- Engine tuning is hitting diminishing returns while gross metrics still rise.
- Metrics improve, but not fast enough to reach a sustainable model.

**Three reasons founders pivot too late**: vanity metrics let you live in a private reality; an unclear hypothesis makes complete failure impossible, so nothing forces the change; fear of public failure.

**What a pivot is**: keep one foot rooted in what you learned; change one fundamental hypothesis about product, business model, or engine of growth. It is not "throw everything out." Wealthfront kept its manager-evaluation technology, which became the core of the new business, and discarded the game.

**The sign of a successful pivot**: the experiments you run afterward are more productive than the ones before.

**Catalog of pivots**:

| Pivot | Change |
|---|---|
| Zoom-in | One feature becomes the whole product |
| Zoom-out | The whole product becomes one feature of a larger product |
| Customer segment | Right problem, wrong customer. Keep the product, change who you serve |
| Customer need | Right customer, wrong problem. Solve a neighboring problem you found through customer intimacy |
| Platform | Application becomes platform, or platform becomes application |
| Business architecture | Switch between high margin / low volume and low margin / high volume |
| Value capture | Change how you monetize. This is intrinsic to the product hypothesis, not a bolt-on |
| Engine of growth | Switch between viral, sticky, and paid |
| Channel | Deliver the same solution through a different sales or distribution channel |
| Technology | Same customer, same problem, same channel, new technology. Usually a sustaining innovation |

**Worked example, Votizen (David Binetti)**, the clearest numeric case in the book:

| Stage | Cost / time | Registration | Activation | Retention | Referral | Revenue |
|---|---|---|---|---|---|---|
| Initial MVP | $1,200 / 3 months | 5% | 17% | too low | too low | n/a |
| After optimization | +$5,000 / 2 months | 17% | 90% | 5% | 4% | n/a |
| More optimization | 3 more months, ~$20,000 and 8 months total | 17% | 90% | 8% | 6% | n/a |
| Zoom-in pivot to @2gov (paid engine) | +$30,000 / 4 months, $50,000 and 12 months total | 42% | 83% | 21% | 54% | <1%, LTV minimal |
| Platform pivot (viral engine) | +1 month | 51% | 92% | 28% | 64% | 11% at $0.20 per message |

Read three things from this table. First, optimization moved retention from 5 to 8 percent in three months; the pivot moved it from 8 to 21 percent in four. Second, MVP cycles accelerated: 8 months, 4, 3, 1. Third, he made quantitative predictions for each leap of faith up front, which is the only reason he could accept failure while gross metrics were still growing.

### 7. Pick and run one engine of growth

Sustainable growth rule: **new customers come from the actions of past customers.** Four sources: word of mouth, side effect of product usage, funded advertising paid from revenue, repeat purchase or use.

Focus on one engine at a time. Dashboards covering all three cause confusion.

**Sticky engine**
- For products with high switching costs or constant repeat use.
- Track the churn rate: the fraction of customers in a period who fail to remain engaged.
- Rate of compounding = natural growth rate of new customers − churn rate.
- Grows if new-customer acquisition exceeds churn. Compounds like interest.
- Diagnostic: one startup had a 61 percent retention rate and 39 percent new-customer growth. Compounding growth was 0.02 percent, almost zero. It looked healthy on totals.
- Counterintuitive fix: when a sticky business stalls, do not spend more on sales and marketing. Improve retention: better inventory, better listings, reasons to come back, limited-time offers.
- Activation rate and revenue per customer barely affect growth here. Use them to test the value hypothesis instead.

**Viral engine**
- Growth happens as a necessary side effect of normal product use, not through deliberate evangelism. Viruses are not optional.
- Track the viral coefficient: how many new customers each new customer brings.
- Below 1.0 the loop fizzles. At 0.1, 100 signups produce 10, then 1, then nothing. Above 1.0 it grows exponentially. At 0.9 or more you are on the verge of success.
- Remove every point of friction in signup and invitation. This is why viral products often do not charge users directly and monetize through advertising instead.
- Hotmail's entire change was one line at the bottom of every e-mail: "P.S. Get your free e-mail at Hotmail," with a link. 1 million users in six months, 2 million five weeks later.
- Value hypothesis still needs a voluntary exchange of value; it just may not be money.

**Paid engine**
- Track customer lifetime value (LTV) and cost per acquisition (CPA). $100 of ads producing 50 signups is a $2.00 CPA.
- Grows while LTV > CPA. Marginal profit sets the speed.
- Increase growth in only two ways: raise revenue per customer, or lower acquisition cost.
- Includes outbound sales teams and retail foot traffic, not just ads.
- Long-run warning: competition bids CPA up until everyone pays away most of their marginal profit. Winning long-term with the paid engine requires a *differentiated* ability to monetize a specific set of customers. IMVU could pay more for teenagers and low-income users because it built payment methods for people without credit cards.

**Product/market fit**: "if you are asking, you're not there yet." Use engine metrics plus innovation accounting to judge direction and rate of progress, not raw levels. A company compounding 0.1 → 0.5 → 2.0 → 3.2 → 4.5 → 5.0 percent is doing better than one flat at ~9.8 percent.

**Every engine eventually runs out.** It is tied to one set of customers, habits, and channels. Because vanity metrics keep rising while the engine coasts, the stall arrives as a surprise crisis. Watch cohort yield, not totals.

### 8. Regulate speed with the Five Whys

Purpose: tie process investment to actual pain, so you never build process speculatively and never skip it when it hurts.

1. Trigger a session automatically on a defined class of failure: a technical fault, a missed business result, an unexpected change in customer behavior.
2. Ask "why" five times until you reach a human or systemic cause. Every seemingly technical problem has a human problem at its root.
3. At each of the five levels, make a **proportional investment**: small symptom, small fix; large symptom, large fix. Assign an owner and a concrete action for each level.
4. Do not drop everything to build the full solution. Do the first hour of the eight-week plan. If the problem recurs, the next session forces more progress. If it does not recur, you lost an hour.

Example from IMVU, exactly as the book gives it:
1. A new release disabled a feature. Why? A particular server failed.
2. Why did the server fail? An obscure subsystem was used the wrong way.
3. Why was it used wrong? The engineer did not know how to use it properly.
4. Why not? He was never trained.
5. Why wasn't he trained? His manager does not believe in training new engineers because the team is "too busy."

That is how IMVU's new-hire training program got built: incrementally, never as a project.

**Rules for running it:**
- Everyone connected to the problem must be in the room, including whoever found it, whoever fixed the symptom, whoever owns the subsystem, and any executive who was escalated to. Whoever is absent becomes the scapegoat.
- Senior people repeat the mantra: "if a mistake happens, shame on us for making it so easy to make that mistake."
- Appoint a Five Whys master per area: senior enough to enforce assignments, junior enough to actually attend every meeting.
- Start small and specific. Pick one narrow symptom class with a simple, ironclad trigger rule (for example, every complaint involving a credit card transaction). Do not start with your accumulated baggage; baggage issues surface organically, and if they never do, they were not as big as they seemed.
- Spend a few minutes at the start of each session explaining the process to newcomers, using a past example.
- Watch for the Five Blames. The goal is the objective truth that chronic problems are caused by bad process, not bad people.

**Simplified version** when trust or authority is missing:
1. Be tolerant of all mistakes the first time.
2. Never allow the same mistake to be made twice.

Solo variant: whenever something goes wrong, ask "how could I prevent myself from being in this situation ever again?"

### 9. Institutionalize experimentation (for teams and larger companies)

**Three structural requirements for any innovation team:**
1. Scarce but secure resources. Small budget, absolutely protected from mid-course raids. Too much budget is as harmful as too little.
2. Independent development authority. Cross-functional, full-time, able to build and ship real products without a queue of approvals.
3. A personal stake in the outcome. Equity, or long-term-linked bonus, or at minimum public credit and named ownership.

**The innovation sandbox** (seven rules, verbatim in structure):
1. Any team can create a true split-test experiment affecting only the sandboxed parts of the product, or only certain customer segments or territories.
2. One team must see the whole experiment through from end to end.
3. No experiment runs longer than a specified time (a few weeks for feature experiments, longer for disruptive ones).
4. No experiment affects more than a specified number of customers, usually a percentage of the mainstream base.
5. Every experiment is evaluated on a single standard report of five to ten actionable metrics, no more.
6. Every team and every product in the sandbox uses the same metrics.
7. The team monitors metrics and customer reactions during the experiment and aborts it if something catastrophic happens.

Start the sandbox tiny. One company started with only the pricing page, then added the home page, then search, then the whole design.

Protect the parent organization from the startup, not the reverse. Hidden skunkworks teams create paranoia and politics, and rarely produce sustained innovation.

**Cadence proof that this scales**: Intuit's TurboTax team runs over 500 changes in a two-and-a-half-month tax season, up to 70 tests per week: change live Thursday, run over the weekend, read results Monday, conclude Tuesday, rebuild Thursday, launch Thursday night.

**QuickBooks turnaround**, the clearest large-company transition:
- Year 1, waterfall: 3-4 months planning, 6-9 months building, first real feedback at launch. The online banking release made reconciliation four to five times slower, dropped Net Promoter Score by 20 points, and took nine months to fix.
- Year 2: cut the cycle in half by decree. Failed. "Organizations have muscle memory."
- Year 3: threw out the old process publicly and invested in the process, product, and technology that make small batches possible. Teams capped at five people. Twenty to twenty-five branches instead of five. Each team runs one feature end to end in about six weeks, testing with real customers throughout. Cross-functional teams formed around ideas; customers involved from the inception of each feature. Result: higher satisfaction, more units sold.
- The enabling investment was technical: a virtualization system that let a second QuickBooks version read real customer data without being able to change it permanently. That removed the data-corruption risk that made small batches impossible.

## Rules and heuristics

| Rule | Why | Failure mode if ignored |
|---|---|---|
| Turn every leap of faith into a number before you build | Only an explicit prediction can be refuted | You declare success retroactively and stay in the land of the living dead |
| Test the riskiest assumption first | If you cannot mitigate it, the others do not matter | You spend months validating things that were never in doubt |
| Ship the MVP before you are comfortable | Delay prevents the feedback you need | You launch a fully formed product into a market that does not want it |
| Sell to early adopters, not the mainstream | They accept an 80 percent solution and give feedback | You over-polish, spend the budget, and still learn nothing |
| Charge money from day one, even tiny amounts | A voluntary exchange of value is the real test of the value hypothesis | You mistake free usage for demand |
| Set small, absolute revenue targets early ($300, then $350, then $400) | Quantitative failure creates the motivation and the questions for qualitative inquiry | You talk to customers with no urgent question and dismiss the answers |
| Report cohorts, never cumulative totals | Each cohort is an independent report card immune to excuses about legacy users or market conditions | Rising totals hide a flat conversion rate for months |
| Split-test every feature, regardless of who requested it | Merit beats job title; most "improvements" change nothing | Seniority decides the roadmap and you never learn what works |
| A story is not done until it is validated | Otherwise "done" means "built," which is not progress | You accumulate features nobody uses and cannot remove them |
| Buy a small daily stream of traffic to measure against | You need enough users per day for real numbers | You wait weeks between report cards |
| Make a proportional investment in prevention | Small pain, small fix keeps process from either bloating or being skipped | Either bureaucracy or repeated firefighting |
| Pick one engine of growth and focus on its metrics | Each engine has different levers; the wrong lever does nothing | You spend on marketing when the real problem is churn |
| Measure runway in pivots, not months | Cutting costs can cut the feedback loop itself | You go out of business more slowly |
| Launch quietly, market loudly later | Brand risk comes from loud promises, not from obscurity | Press expectations you cannot meet, plus feedback from the wrong audience |
| Everyone affected attends the root-cause meeting | The absent person becomes the scapegoat | Blame replaces learning |

## Anti-patterns

| Anti-pattern | What it looks like | Fix |
|---|---|---|
| Achieving failure | Executing a well-made plan faithfully and on time, into a market that was never there | Convert the plan into testable hypotheses and test before committing infrastructure and hiring |
| Vanity metrics | Board slides of total users, total revenue, hits, all "up and to the right" | Cohort funnels and split tests; the three A's |
| Success theater | Last-minute ad buys, channel stuffing, whiz-bang demos, premature PR to make the numbers look good | Innovation accounting; report engine drivers instead |
| The audacity of zero | Delaying any data collection because zero invites imagination and small numbers invite doubt | Ship early, set explicit small targets, teach stakeholders the language of validated learning |
| "Just do it" / JFDI | Ship and see what happens | You are guaranteed to succeed at seeing what happens. Define the hypothesis so failure is possible |
| Analysis paralysis | Endless refining of plans, research reports, whiteboard strategizing | The errors are in product-customer interaction and are invisible at the whiteboard. Build an MVP |
| Learning as an excuse | Rationalizing a failed cycle by claiming valuable lessons, with no evidence | Turn it into validated learning in the *next* cycle by moving a metric |
| Optimizing the wrong thing | Months of usability tweaks, incentive programs, and A/B wins with no movement in the engine drivers | Recognize diminishing returns as the classic pivot signal |
| Capitulating to customers | Building exactly what users say they want (IMVU's single-player mode) | Seek a synthesis between your vision and what customers will accept. Watch behavior, not requests |
| Copying industry best practices untested | Grockit's lazy registration, kept because "everyone does it" | Split-test the best practice against not doing it |
| Hiding the innovation team | Secret skunkworks sprung on the organization after success | Innovation sandbox in the open, with shared standard metrics |
| Large-batch death spiral | Release dates receding, "one more feature," bet-the-company launches | Cut batch size; invest in the tooling that makes small batches safe |
| The Five Blames | Root-cause sessions turning into finger-pointing | Full attendance, the "shame on us" mantra, start with a narrow low-stakes symptom |
| Trusting the engine for your own success | Growth is coming from an engine that already works, not from your current work | Cohort yield per new group, not aggregate growth |
| Founders following their product forever | The inventor gets stuck running optimization of what they created | Manage four phases (R&D, growth, optimization, legacy) as separate teams with handoffs; treat "entrepreneur" as a job title |

## Quotes worth keeping

- "A startup is a human institution designed to create a new product or service under conditions of extreme uncertainty."
  Use when someone argues the method does not apply because they are not a garage startup.
- "if you cannot fail, you cannot learn."
  Use when a test is designed so that no possible result would change your plan.
- "The lesson of the MVP is that any additional work beyond what was required to start learning is waste, no matter how important it might have seemed at the time."
  Use when scoping the first release and everything feels essential.
- "If we do not know who the customer is, we do not know what quality is."
  Use when the team wants to delay shipping until quality is acceptable.
- "The only way to win is to learn faster than anyone else."
  Use against stealth mode and against fear of copycats.
- "a good design is one that changes customer behavior for the better."
  Use when judging a redesign that everyone likes but that moved no metric.
- "Success is not delivering a feature; success is learning how to solve the customer's problem."
  Use to reset what "done" means for a sprint.
- "New customers come from the actions of past customers."
  Use to separate real growth from one-time spikes and publicity.
- "The true measure of runway is how many pivots a startup has left"
  Use when deciding what to cut in a cash crunch.
- "Startups don't starve; they drown."
  Use when the backlog is full of marginal optimizations.
- "if a mistake happens, shame on us for making it so easy to make that mistake"
  Use at the start of any post-mortem.
- "There is surely nothing quite so useless as doing with great efficiency what should not be done at all."
  Peter Drucker, quoted by Ries. Use against velocity metrics.

## Applies to

**Idea validation.** This is the book's strongest domain. Leap-of-faith assumptions, smoke tests, concierge and Wizard-of-Oz MVPs, and the Kodak four questions give you a complete procedure for testing an idea before writing code. The Zappos, Groupon, and Food on the Table cases are directly copyable for a SaaS founder: sell first, deliver by hand, automate only when you are too busy to keep up.

**Positioning.** Covered indirectly but usefully. IMVU changed one phrase, "avatar chat" to "3D instant messaging," across the site and registration flow, split-tested it, and got more signups *and* more long-term paying customers. Grockit's registration test proved customers decided on positioning and marketing rather than on product experience. Treat positioning as a first-class split test, not copywriting.

**Pricing.** Thin. The value-capture pivot says monetization is intrinsic to the product hypothesis, not a feature you add later. The Village Laundry case shows price discovery through iteration: customers paid double for a four-hour turnaround instead of twenty-four. The multi-segment pricing conflict (enterprise discounts blocking consumer price experiments) is described as a political problem solved by the sandbox. No pricing model, no willingness-to-pay method.

**Landing page and CRO.** Directly applicable. The smoke test is a landing-page preorder. Split testing, cohort funnels, and the three A's are exactly a CRO discipline. The $5-per-day traffic buy is a cheap way to get statistically usable daily cohorts on a new page.

**Onboarding and activation.** Applicable with a caveat. Activation rate is one of the named funnel stages, and Votizen moved activation from 17 to 90 percent through split testing in two months for $5,000. The caveat is IMVU's failure: they spent months raising activation with usability work, persuasion techniques, incentives, and quests, and the engine did not move. Activation work pays only when activation is actually a driver of your engine.

**Retention and churn.** Central to the sticky engine. Churn rate is defined precisely, and rate of compounding = growth rate − churn rate. The key prescription is counterintuitive and worth keeping: a stalled sticky business should invest in retention, not in more sales and marketing.

**Growth.** The three engines chapter is the operational core. Pick one, learn its single controlling number (compounding rate, viral coefficient, LTV−CPA margin), and ignore work that does not move it.

**Product decisions.** The kanban validation gate, the split-test-everything norm, the pivot catalog, and the pivot-or-persevere meeting are a complete decision system for what to build next and when to stop.

## Conflicts and limits

- **It does not tell you what to build.** Ries is explicit that vision, intuition, and judgment cannot be removed. The method tells you how to test an idea, not how to have one. Pair it with a positioning or customer-research method.
- **It contests "listen to your customers."** Ries says customers cannot tell you what they want, and IMVU's single-player mode is his proof that literal compliance with requests fails. This clashes with jobs-to-be-done and customer-interview schools that treat interview output as direction. The reconciliation Ries offers: interviews generate hypotheses, behavior validates them.
- **It contests "quality first."** The MVP argument directly opposes craft-led approaches, Six Sigma, and design thinking's polished deliverable. Ries carves out an exception: defects that slow the Build-Measure-Learn loop are never acceptable, and mainstream customers are far less forgiving than early adopters. IMVU's own near-death came from applying the low-quality MVP rule too long after it stopped applying.
- **Split-test-everything conflicts with brand and craft work.** Some of the highest-value changes (IMVU's major redesign) initially perform *worse* than the old version and need months of protected investment. The book admits this but gives no rule for when to protect a change from its own early numbers.
- **The statistics are absent.** There is no discussion of sample size, significance, test duration, or the risk of many simultaneous tests. Running 70 tests per week, as Intuit does, raises false-positive problems the book never mentions. Bring your own statistical discipline.
- **Low-traffic products are underserved.** Cohort analysis and split testing assume enough users per period for real numbers. A B2B SaaS with 40 trials a month cannot run the IMVU playbook. The concierge MVP and customer conversations are the parts that survive at low volume.
- **The viral coefficient is presented as simple and is not.** Cycle time, decay, and channel saturation are ignored. A stated coefficient of 0.9 as "on the verge of success" is a heuristic, not a model.
- **Pricing, sales process, unit economics, and positioning frameworks are outside the book's scope.** LTV and CPA appear only as ratios; there is no cohort LTV model, no payback period, no discussion of expansion revenue.
- **Survivorship bias in the cases.** Nearly every example is a company that succeeded, several of which Ries had an equity or advisory interest in (Aardvark, Dropbox, Food on the Table, Grockit, IMVU, Intuit, Votizen, Wealthfront; disclosed in the book). The counterfactual, startups that ran this method and still failed, is absent.
- **Age of the material.** Published 2011. All figures are as of then. Some named companies have since changed substantially. Do not cite the outcomes as current.
- **Source text defects.** The extracted file has systematically lost the "fi", "fl", "ffi", and "ff" ligatures, so words appear as "scienti c", "e ciency", "e ort", " rst", " gure". Many lines are duplicated where page headers repeat. All figures, charts, and diagrams are missing: the IMVU cohort graph, the IMVU vanity-metrics graph, the kanban diagram, and the viral-coefficient chart are referenced but not present, so the exact plotted numbers behind them are not observable. The kanban cap of three per bucket comes from the diagram caption, which did survive. Where the source gave only a caption or a "see chart" reference with no data, no numbers are reported here.
