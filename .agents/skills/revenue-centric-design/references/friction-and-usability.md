# Friction & Usability (Krug)

> Distilled from **Steve Krug, _Don't Make Me Think, Revisited_ (3rd ed.)**. This is the **friction lens**: it does not
> tell you what to build or who to build it for — the rest of this skill does that. It tells you whether the thing you
> designed can actually be operated by a distracted human moving at speed.
>
> Position in the chain: `ICP/persona → journey + conversion goal → screen design → **friction audit (this file)** → usability test`.
> Krug runs **after** the design exists, as critique. Using it as a generation prompt wastes it.

## The three laws

1. **Don't make me think.** Every page should be self-evident. If not self-evident, then self-explanatory. Your job is to get rid of the question marks.
2. **It doesn't matter how many clicks, as long as each click is a mindless, unambiguous choice.** Depth is not the enemy; ambiguity is.
3. **Get rid of half the words on each page, then get rid of half of what's left.**

---

## Eliminate the question marks — self-evident beats self-explanatory
**Principle.** Every element that makes a user stop and ask "what is that?" spends cognitive budget that belonged to the task. The distractions are individually tiny and they compound, especially on actions users take constantly (deciding what to click).
**Apply when.** Naming anything (nav labels, buttons, sections, features, plans), or reviewing any screen before ship.
**The move.** Hunt the question marks: cute/clever names, marketing-invented names, company-internal names, unfamiliar technical names. Every naming tradeoff should skew further toward "Obvious" than instinct suggests. The standard is that a neighbor with zero interest in your domain looks at the page and says "Oh, it's a ___." If you genuinely cannot make something self-evident (original or inherently complex product), settle for **self-explanatory**: size, color, layout, well-chosen names and small amounts of crafted text combine into near-effortless understanding.
**Evidence.** Krug's list of things users should never have to think about: *Where am I? Where do I begin? Where did they put ___? What are the most important things on this page? Why did they call it that? Is that an ad or part of the site?*
**Trap.** "There's almost always a plausible rationale — and a good, if misguided, intention — behind every usability flaw." A defensible reason for a confusing label does not make it less confusing.
**Voice.** "When you're creating a site, your job is to get rid of the question marks."

## Design for scanning, satisficing, and muddling through
**Principle.** Three facts govern real use, and every one of them contradicts how teams imagine their users behave.
**Apply when.** Any time someone argues "users will read this" or "users will compare the options."
**The move.** Design against all three:
- **We don't read, we scan.** Users are on a mission, know they don't need everything, and are lifelong expert scanners. They lock onto words matching the task at hand, their ongoing interests, and hardwired trigger words.
- **We don't optimize, we satisfice.** Users pick the *first reasonable option*, not the best one — because they're in a hurry, the penalty for guessing wrong is one Back click, weighing options doesn't help on a poorly designed site, and guessing is more fun. So your first plausible-looking link absorbs the traffic, correct or not.
- **We don't figure things out, we muddle through.** People use products effectively with completely wrong mental models and never look for a better way once something works. This is not a beginner trait; experts muddle at a higher level.
**Evidence.** Gary Klein's naturalistic decision-making research: fire commanders under time pressure didn't compare *any* options — they took the first workable plan and ran a quick mental test on it. Herbert Simon coined *satisficing* in 1957.
**Why it still matters if they muddle through.** Users who "get it" find more, see the full range of what you offer, can be steered where you want them, and feel smart — which brings them back. "You can get away with a site that people muddle through only until someone builds one down the street that makes them feel smart."
**Voice.** "We're thinking 'great literature'; the user's reality is 'billboard going by at 60 miles an hour.' If your audience is going to act like you're designing billboards, then design great billboards."

## Use conventions — clarity trumps consistency
**Principle.** Conventions are pre-paid comprehension. Users already know where the logo goes, what a cart is, what a magnifying glass means. Reinventing them charges the user for what they already owned.
**Apply when.** You feel the pull to do something novel with navigation, controls, iconography, or layout.
**The move.** If you're not using an existing convention, your replacement must either (a) be so clear and self-explanatory there's no learning curve, or (b) add so much value it's worth a small one. **Innovate when you know you have a better idea; take advantage of conventions when you don't.** Be as creative and aesthetically ambitious as you want, as long as it stays usable.
**Rule.** **CLARITY TRUMPS CONSISTENCY.** If you can make something significantly clearer by making it slightly inconsistent, choose clarity. Consistency is a good default, not a trump card in design arguments.
**Trap.** Designers resist conventions because praise, awards, and job offers are never given for "best use of conventions." Custom scrollbars are the canonical failure: nobody replicates the thousands of hours of tuning behind the OS default.
**Evidence.** Stop signs and car pedals: standardized shape, color, size, and position is exactly why they work at a glance, at distance, in bad conditions.

## Build a real visual hierarchy — it preprocesses the page
**Principle.** Visual appearance must accurately encode the actual relationships: what's important, what's similar, what's part of what. A good hierarchy does the parsing work *for* the user before they read a word.
**Apply when.** Every screen. This is the highest-leverage structural fix and the most common structural failure.
**The move.** Three traits, all required:
- **More important = more prominent.** Larger, bolder, distinctive color, more white space, nearer the top — or a combination.
- **Related logically = related visually.** Group under a heading, share a visual style, or enclose in a defined area.
- **Nested visually to show what's part of what.** A section heading must span exactly the elements it governs — no more, no less.
**Failure mode.** When everything looks equally important, users fall back to the slow process of scanning for revealing words and inventing their own sense of structure. A *slightly* flawed hierarchy is worse than obviously flawed: it reads like a carelessly built sentence ("Bill put the cat on the table for a minute because it was a little wobbly") — decodable, but it throws you.
**Evidence.** Every newspaper page conveys relative importance through prominence, grouping, and nesting before you read a word.

## Break the page into clearly defined areas
**Principle.** Users decide in the first glances which regions of a page are worth attention, then rarely look at the rest — as though it weren't there.
**Apply when.** Laying out any dense screen: dashboards, home pages, marketplace listings, settings.
**The move.** A user should be able to point at each region and name it: "things I can do here," "navigation," "what they're selling me." If a region can't be named at a glance, it will be ignored or it will steal attention from a region that mattered.
**Evidence.** Eye-tracking studies of page scanning. Banner blindness is just the extreme case of a general behavior.

## Make it obvious what's clickable
**Principle.** A large share of what users are doing is *looking for the next thing to click*. Clickability must be readable from shape, location, and formatting alone.
**Apply when.** Any interactive element, and especially on touch targets.
**The move.** Stick to one color for text links, or make shape and location carry the signal. Never use the same color for links and non-clickable headings. On mobile there is **no cursor, so no hover** — tool tips, hover color changes, and hover-revealed menus simply do not exist for those users; replace them, don't assume them.
**Related term.** *Affordances* (Norman's "signifiers"): visual clues suggesting how a thing is used. A bordered box says "type here." Remove the border and the function survives only for users who already knew.
**Flat design tradeoff.** Flat design strips visual distinctions — decoration *and* the information the texture was carrying. Affordance cues are usually multi-dimensional (position + formatting). If you go flat, deliberately use the remaining dimensions to compensate for what you removed.

## Keep the noise down
**Principle.** Visual noise is the enemy of grasp-at-a-glance. It comes in three distinct forms, each with a different fix.
**Apply when.** Any screen that feels busy, and every home/landing page review.
**The move.** Diagnose which noise you have:
- **Shouting.** Everything clamors at once. This is a symptom, not a cause: it's the residue of failing to make the hard call about what's actually most important.
- **Disorganization.** Elements strewn without alignment. Sign the designer isn't using a grid.
- **Clutter.** Simply too much stuff, producing a low signal-to-noise ratio where the noise obscures the useful content.
**Editing stance.** Start from **"everything is visual noise — presumed guilty until proven innocent"** and remove anything not making a real contribution.

## Format text to support scanning
**Principle.** Most of the time users spend on your text is spent scanning it for something. Formatting is what makes that possible.
**Apply when.** Any content-bearing screen, docs, empty states, or long-form marketing.
**The move.**
- **Use plenty of headings** — more than you think, and spend more time writing them. They act as an informal outline that lets people decide what to read, scan, or skip.
- **Style headings correctly.** Make level distinctions impossible to miss (size or space above). Critically: **don't let headings float** — a heading must sit closer to the section it introduces than the one it follows.
- **Keep paragraphs short.** Long paragraphs are a "wall of words" (Jarrett & Redish). Single-sentence paragraphs are fine. Any long paragraph almost always has a reasonable break point.
- **Use bulleted lists.** Almost anything that *can* be a bulleted list probably should be — look for any series separated by commas or semicolons. Add a little space between items.
- **Highlight key terms** in bold on first appearance. Don't over-highlight or the technique dies.

## Make every choice mindless — or make the guidance brief, timely, unavoidable
**Principle.** What costs users is not the number of clicks but how hard each click is: the thought required and the uncertainty about whether it was right. Confidence that you're on the right track ("scent of information") is what sustains a deep path.
**Apply when.** Any branching choice: plan selection, account-type pickers, "are you a X or a Y?" gates, form questions.
**The move.** Links must unambiguously identify their target so they give off strong scent. Rule of thumb: **three mindless clicks equal one click that requires thought.** When a choice genuinely can't be made simple, don't dump all the detail at once — split it so the user makes a coarse selection first and only then sees the questions relevant to that branch. When you must give guidance, make it:
- **Brief** — the smallest amount that helps
- **Timely** — placed exactly where it's needed
- **Unavoidable** — formatted so it will be noticed
**Failure mode.** Forcing a self-classification the user can't confidently make ("Home Office or Small Business?", "subscriber but not member?"). The question quietly mutates from "how do I answer this?" into "how much do I even want this?"
**Evidence.** London's "LOOK RIGHT" curb markings: brief, timely, unavoidable.
**Voice.** "It doesn't matter how many times I have to click, as long as each click is a mindless, unambiguous choice."

## Omit needless words — happy talk and instructions must die
**Principle.** Most words on most screens are taking up space because nobody will read them. Worse: their presence implies you *must* read them to proceed, which makes the page feel more daunting than it is.
**Apply when.** Every screen, but especially section fronts, welcome states, onboarding, and form intros.
**The move.** Cut half the words, then half of what's left. Removing half is realistic and loses nothing; the second half is the instruction to be ruthless. Kill two specific categories:
- **Happy talk** — content-free welcome/promotional text that says how great you are instead of what makes you great. Test: if you hear "blah blah blah" in the back of your head while reading it, it's happy talk.
- **Instructions** — nobody reads them until repeated muddling has failed, and by then wordy instructions won't be parsed either. Goal is to **eliminate instructions entirely by making things self-explanatory**; when unavoidable, cut to the bare minimum.
**Payoff.** Lower noise, more prominent useful content, shorter pages, more visible per glance.
**Evidence.** Krug's survey-intro rewrite: 103 words → 34 words, more useful.
**Source.** Strunk & White rule 17, "Omit needless words."

## Navigation is the product — persistent navigation and its four jobs
**Principle.** Web space has no scale, no direction, and no accumulated sense of location. Navigation compensates by embodying the hierarchy and creating a sense of "there." Without it, there's no there there.
**Apply when.** Designing any multi-level product surface: app shells, dashboards, docs, marketplaces.
**The move.** Persistent (global) navigation should silently promise: *"the navigation is here, parts change with location, it always works the same way."* It carries **Site ID, Sections, Utilities, Search** (plus a route Home). Details that matter:
- **Site ID** top-left, framing everything, and clickable to Home — it's highest in the hierarchy, so it either dominates or frames.
- **Sections** = primary navigation, the top level of the hierarchy.
- **Utilities** = things outside the content hierarchy (Sign in, Help, Cart, About). Slightly less prominent than Sections; **only four or five fit** — the rest belong in the footer.
- **Search** = a box, a button, the word "Search" or a magnifying glass. Avoid fancy wording (not "Quick Find"), avoid instructions, avoid scope options up front — offer scoping on the *results* page when too many hits prove it's needed.
**The one exception.** Forms. On checkout/registration/feedback pages, persistent nav is a distraction — strip to Site ID, Home, and any utility that helps complete the form.
**Overlooked purposes.** Navigation also (a) tells us **what's here** by making the hierarchy visible — revealing content may matter more than guiding, (b) tells us **how to use the site**, which is all the instruction most users will ever accept, and (c) **builds confidence in the people who built it**.
**Common failure.** Lower-level navigation is designed ad hoc because teams only mock up the home page and two levels. Users spend as much time at lower levels as at the top, and grafting consistency on later is very hard. **Have sample pages showing navigation for every level before arguing about the color scheme.**

## Name every page, and match the name to what was clicked
**Principle.** Page names are the street signs of a product. Unnoticed when things go well; essential the moment a user suspects they're off course.
**Apply when.** Every routed view, modal, and detail screen.
**The move.** Four requirements: **every page has a name**; the name is **in the right place** (framing the content unique to this page, not the nav or chrome); the name is **prominent** (usually the largest text on the page); and the name **matches what I clicked**. Highlighting the page in the nav is not a substitute for a page name.
**The implicit contract.** *The name of the page will match the words I clicked to get there.* Each violation forces a millisecond of "why are those two different?" and erodes trust in the site and its makers. When space forces a compromise, make them as close as possible and make the reason for the difference obvious ("Gifts for Him" → "Gifts for Men" is fine).

## Show "You are here" — and make the cue twice as loud as feels right
**Principle.** Highlighting current location in nav bars, lists, and menus counteracts the Web's inherent lost-in-space feeling.
**Apply when.** Any nav with more than one level, any wizard or multi-step flow.
**The move.** Mark the current section *and* subsection, and apply **more than one visual distinction** (e.g., color *and* bold) so the marker survives a hurried glance.
**Trap.** The most common failure of "you are here" indicators is being too subtle. Designers prize subtlety as sophistication; hurried users miss subtle cues entirely, so a too-quiet indicator adds noise without adding signal. **If you're a designer and you think a visual cue is sticking out like a sore thumb, it probably needs to be twice as prominent.**
**Breadcrumbs.** Best in large, deep hierarchies. Put them at the top (it marginalizes them appropriately, like page numbers), use `>` between levels, and boldface the last item, which is the current page and therefore not a link.

## Run the trunk test
**Principle.** Users are rarely walking your intended path from the home page. They teleport into the middle of your product from a link, a search result, or an email, having never seen your navigation scheme.
**Apply when.** Before shipping any navigational change; as a recurring audit on random deep screens.
**The move.** Pick a page deep in the product at random and print it. Hold it at arm's length or squint so you can't study details. As fast as possible, find and circle:
- What site is this? (**Site ID**)
- What page am I on? (**Page name**)
- What are the major sections? (**Sections / primary nav**)
- What are my options at this level? (**Local navigation**)
- Where am I in the scheme of things? (**"You are here" indicators**)
- How can I search?
**Why blurred.** The test isn't whether you *can* figure it out with time and scrutiny. The standard is that these elements pop off the page regardless of whether anyone is looking closely — you must be judging overall appearance, not details.

## Answer the four questions in the first seconds (Big Bang Theory of design)
**Principle.** The first few seconds on a new product are disproportionately determinative. Snap judgments form in milliseconds and turn out to closely predict considered assessments. Worse, wrong first assumptions get force-fitted onto everything encountered afterward: "if people are lost when they start out, they usually just keep getting loster."
**Apply when.** Home pages, landing pages, first-run screens, and any page that might be someone's entry point (which is all of them).
**The move.** The entry surface must answer, at a glance and unambiguously: **what is this, what can I do here, what do they have here, why should I be here and not somewhere else.** Three places users expect an explicit statement:
- **The tagline**, next to the Site ID — read as a description of the whole product.
- **The welcome blurb**, a terse description in a prominent block, top-left or center.
- **The "learn more"**, often a short explanatory video for novel propositions.
Use as much space as necessary — and no more. Never use a corporate mission statement as a welcome blurb.
**The fifth question.** After "what is this," the entry surface must also answer **where do I start**: here's where to search, here's where to browse, here's where to sample the best stuff, here's where to sign in or start the process. Make entry points *look* like entry points and label them plainly.
**Evidence.** "Attention Web Designers: You Have 50 Milliseconds to Make a Good First Impression!" — initial impressions closely matched considered ones.
**Why it's the thing that gets lost.** Everything else on the page has an internal champion fighting for it. Nobody's job is "make the main point clear," so it's the first casualty of compromise. And **it's the one thing nobody inside the organization can notice is missing** — you must test it with outsiders.

## Taglines: value proposition, not motto
**Principle.** A tagline is the one place users most expect a concise statement of purpose, making it extremely efficient real estate.
**Apply when.** Writing the line next to your logo, or auditing a positioning statement.
**The move.** Good taglines are **clear and informative** (explain exactly what you do), **just long enough** (six to eight words), and **convey differentiation and a clear benefit**. Nielsen's test: a really good tagline is one **nobody else in the world could use except you**. Clever is fine only when the cleverness conveys rather than obscures the benefit.
**Trap.** Don't confuse a tagline with a motto. "We bring good things to life" expresses a guiding ideal; a tagline conveys a value proposition. Mottos are lofty and reassuring and tell a newcomer nothing about what the thing is.

## Protect the entry surface from the tragedy of the commons
**Principle.** Promoting things on the home page works *too* well, so every stakeholder wants a slot. The section promoted captures the entire gain; the resulting clutter cost is shared across all sections. Each stakeholder's rational move is to add one more thing, so the commons is doomed.
**Apply when.** Home page, dashboard, or app-shell real estate negotiations; anywhere "can we just add one more banner" recurs.
**The move.** Treat it as a commons requiring active defense, because degradation is gradual — the slow, inexorable addition of just one more thing. Educate stakeholders on overgrazing and offer alternatives: cross-promote from other high-traffic pages, or rotate stakeholders through the same slot.
**Evidence.** Hardin's "Tragedy of the Commons" (Science, 1968).

## Stop religious debates — test instead of arguing about preferences
**Principle.** Teams burn enormous time on unresolvable debates about what users "like," because everyone on the team is also a user with strong convictions and a natural tendency to project those preferences onto users at large.
**Apply when.** Any design discussion that has cycled twice without new information. Any argument phrased as "users like/hate X."
**The move.** Replace the unanswerable question with an answerable one. Not *"do people like dropdown menus?"* but ***"does this dropdown, with these items and this wording, in this context on this page, create a good experience for most people likely to use this?"*** There's exactly one way to answer that: build a version, even a crude one, and watch people try to use it.
**Two forces making the debates inevitable.** Personal passion (we assume users are like us) and professional passion (designers optimize for visual pleasure, developers for interesting complexity, because those are brain-chemistry rewards) — layered under a broader clash between the *hype culture* (management, marketing, bizdev, making promises) and the *craft culture* (designers and developers, delivering on them).
**The deeper myth.** There is no Average User. **All users are unique and all use is basically idiosyncratic.** The myth's real damage is that it reinforces the idea that good design is a matter of figuring out what people like, when what actually works is well-integrated design that fills a need — carefully thought out, well executed, and tested.
**Voice.** "People often test to decide which color drapes are best, only to learn that they forgot to put windows in the room."

## Do-it-yourself usability testing: three users, one morning, every month
**Principle.** Testing is qualitative and diagnostic, not statistical proof. Its purpose is to find and fix problems, and it works at absurdly small scale.
**Apply when.** Continuously, from before design starts through post-launch. Not as a pre-launch disaster check.
**The move.**
- **Cadence.** One morning a month: test three users, debrief over lunch, leave with an agreed fix list. Pick a fixed day (e.g., the third Thursday) rather than tying testing to milestones, because milestones slip and testing slips with them. On agile cycles, two users every two weeks — the fixed schedule is the point.
- **Why three.** You'll never find all problems, and **you can find more problems in half a day than you can fix in a month**. Three users hit most of the significant problems for the tasks tested. More rounds beat wringing more out of each round.
- **Recruiting.** **Recruit loosely and grade on a curve.** Try to find representative users, don't get hung up on it, and mentally adjust: "would our users have this problem, or only because they lack what our users know?" Deliberately include some participants outside the target audience — it's bad to design something only your target audience can use, we're all beginners under the skin, and experts are never insulted by genuine clarity.
- **Structure (1 hour).** Welcome (4 min) → background questions (2 min) → home page tour (3 min: "tell me what you make of this, don't click yet") → **tasks (35 min)** → probing (5 min) → wrap-up (5 min).
- **Facilitation.** The main job is keeping the participant thinking out loud. Prompt with "What are you thinking?", "What are you looking at?", "What are you doing now?" Do not lead, do not assist unless they're hopelessly stuck; deflect help requests with **"What would you do if I wasn't here?"** Save all probing questions for the end so you don't bias the run.
- **Task wording.** Word tasks carefully and supply information they'd need but wouldn't have. Let participants choose some details ("find a book you'd actually buy" beats "find a cookbook under $14") — it raises emotional investment and lets them use real personal knowledge.
- **Observers.** As many as possible; watching a test is transformative and is the single best tool for making stakeholders understand users aren't like them. Each observer writes down their three most serious problems per session.
**Debrief method.** Collect everyone's top three into a collective list (observed problems only, no discussion yet) → choose the ten most serious → rank 1–10 → for each, write a rough fix, an owner, and required resources → **stop when you've allocated the month's available capacity**.
**Rule.** **FOCUS RUTHLESSLY ON FIXING THE MOST SERIOUS PROBLEMS FIRST.** The common failure is opting for low-hanging fruit over one serious problem, which is why serious usability defects survive on large, well-funded products.
**What to ignore.**
- **"Kayak" problems.** Users who veer off then self-correct almost immediately without help and without being fazed. If a user's second guess is always right, that's good enough.
- **New-feature requests.** Ask the participant to describe how the feature would work; they usually conclude "actually I probably wouldn't use that." Participants aren't designers — when they do have a great idea you'll know instantly, because your reaction will be "why didn't we think of that?"
- **Color comments.** Ignore aesthetic remarks unless three of four participants reach for a word like "puke."
**Resist adding.** When users don't get something, the reflex is to add an explanation. Usually the right fix is to **take away** what's obscuring the meaning, not add another distraction.
**Focus groups ≠ usability tests.** Focus groups gather opinions in the abstract and belong in *planning* (is this the right product? is the value proposition attractive?). Usability tests watch **one person at a time actually use the thing** and belong throughout the whole process.
**Typical problems you'll see.** (1) Users are unclear on the concept. (2) The words they're looking for aren't there. (3) There's too much going on — the thing is right there and they don't see it, so cut noise or raise its prominence in the hierarchy.
**Voice.** "Testing one user is 100 percent better than testing none. Testing one user early in the project is better than testing 50 near the end."

## Mobile: constraints force tradeoffs, and bad tradeoffs are where usability dies
**Principle.** Design is constraints plus tradeoffs. **Most serious usability problems are the result of a poor decision about a tradeoff** — not of nobody having thought about it.
**Apply when.** Any small-screen or responsive work; any "we had to compromise because of X" explanation.
**The move.** Assume every ugly pattern was debated and compromised, then check whether the compromise weighted the user's experience enough. Specific guidance:
- **Don't scope by imagined context.** Mobile First is right about forcing prioritization but wrong when read as "include only what people need on the move." People use phones on the couch and expect to do everything. If you include everything, prioritize harder: frequent or urgent things close at hand, everything else a few taps away **with an obvious path**.
- **Depth is acceptable.** Small screens mean more tapping and scrolling — fine, as long as the user stays confident what they want is further down or behind that control.
- **Rule.** **Managing real-estate challenges shouldn't be done at the cost of usability.**
- **Don't strand the user.** Deep links must land on the linked content, not the mobile home page. Allow zooming. Provide a route to the full site.
- **Speed is a feature.** Slow performance equals frustration and lost goodwill; mobile connection quality varies wildly. Watch payload size in responsive solutions.
**Learnability and memorability.** Krug's working definition of usability: *a person of average or below-average ability and experience can figure out how to use the thing (learnable) to accomplish something (effective) without it being more trouble than it's worth (efficient).* Two extra attributes bite hardest on apps: **learnable** (novel gestures and navigation create a lot to learn, and help is often unfindable — a Catch-22 when you can't navigate to the help) and **memorable** (if relearning costs as much as learning, users abandon; the best route to memorable is being genuinely easy to learn the first time). Delight is the extra-credit assignment — pursue it, but not at the cost of usability.

## Be a mensch — the reservoir of goodwill
**Principle.** Every user arrives with a reservoir of goodwill. Each problem lowers it. Beyond "is my site clear?" you must ask **"does my site behave like a mensch?"**
**Apply when.** Pricing disclosure, support access, form design, error states, outages, cancellation, and any moment where the business interest and the user interest diverge.
**The move.** Know the reservoir's properties: it's **idiosyncratic** (you can't count on a large reserve), **situational** (it may already be low before they reach you), **refillable** (you can restore it by visibly acting in their interest), and **sometimes emptied by a single mistake** (a registration form with too many fields can take it to zero instantly).
**What drains it.**
- **Hiding what I want** — support numbers, shipping rates, prices. Hiding the phone number to deflect calls just makes people angrier when they finally find it; a visible number often keeps people self-serving *longer*, because knowing they *can* call is enough.
- **Punishing me for not doing things your way** — rejecting spaces in a card number, dashes in an ID. Don't make me jump through hoops because you didn't want to write a little code.
- **Asking for information you don't need.**
- **Shucking and jiving** — faux sincerity, "your call is important to us."
- **Putting sizzle in my way** — bloated feel-good marketing between me and my task.
- **Looking amateurish** — though note almost nobody leaves purely over aesthetics.
**What refills it.** Know the three main things people come to do and make them obvious and easy. Tell me what I want to know, especially what you'd rather not disclose — you lose points on the fee and gain more for candor. Save me steps. Put visible effort in. Answer the questions I'm actually likely to have (real FAQs, kept current from this week's top support questions, and candid — not QWWPWAs: "Questions We Wish People Would Ask"). Make errors easy to recover from. **When in doubt, apologize** — if you can't do what they want, at least acknowledge the inconvenience.
**Business-decision caveat.** You may deliberately choose a goodwill-draining pattern for revenue. Fine — just do it **in an informed way rather than inadvertently**.

## Accessibility: fix what confuses everyone first
**Principle.** You can't call a product usable unless it's accessible. But the highest-impact accessibility work is not the compliance checklist — it's the clarity work you should be doing anyway.
**Apply when.** Any accessibility pass; any time the team frames accessibility as a separate compliance workstream.
**The move.** In order:
1. **Fix the usability problems that confuse everyone.** If something confuses most users, it will certainly confuse users with disabilities, and they'll have a harder time recovering. Applying accessibility guidelines to an unclear product is lipstick on a pig. Test often, smooth out shared confusion.
2. **Learn what screen reader use actually looks like** — Theofanos & Redish's observation study of 16 blind users is the fastest way in.
3. **Take the low-hanging fruit:** meaningful `alt` text on every image (empty `alt=""` for decorative ones); correct heading structure (`h1` for the page title, `h2` for major sections, and so on, styled via CSS); form fields associated with `<label>`; a "Skip to Main Content" link; all content reachable by keyboard; significant text/background contrast; an accessible template or theme.
**Key insight from the research.** **Screen-reader users scan with their ears.** They're just as impatient as sighted users, often at very high speech rates, and they listen to only the **first few words of a link or line** before moving on. A sighted user can find a keyword anywhere on the page; a screen-reader user may never hear it unless it's at the *start* of the link or line. **Front-load your link text and headings.**
**Framing.** The two standard arguments (percentage-of-population, "helps everyone") tend to breed skepticism in young developers and obscure the real reason: it's the right thing to do, and it dramatically improves some people's lives. Expect a legislative stick eventually regardless.
**The real fear to address.** Designers fear "buttered cats" — cases where good design for disabled users directly opposes good design for everyone else. Genuine conflicts are far rarer than feared; the Chicago taxi sign with Braille embossed on overlaid Plexiglas is the model, where each audience got the best possible experience instead of both being halved.

## Make usability happen where you live
**Principle.** Getting an organization to take usability seriously is a political problem, not a technical one, and the ROI-proof route is expensive and always contestable.
**Apply when.** You're the only person advocating for users, or you need budget and permission for research.
**The move.** The highest-leverage tactic: **get your boss (and their boss) to watch one usability test, live.** Executives routinely stay longer than planned because it's the first time they've seen anyone actually try to use their product, and the picture is rarely as pretty as they imagined. Live beats a recap the way a live game beats the evening news. If they won't come, use clips under three minutes.
**Supporting tactics.** Do the first test on your own time — don't ask permission, keep it informal, use volunteers so it costs nothing. Pick an easy target with at least one serious, quickly fixable problem (a badly labeled button), then test it, fix it, measure if you can, and publicize it. **Test a competitor** — everyone loves learning about the competition and nobody has anything personally on the line. Empathize genuinely with management's actual position. Keep some humility: your role is to share what you know, not to bring the truth to the unwashed masses.

---

## Applying this file to agent-built design

- **Krug is a critique lens, not a generation lens.** Generate with the rest of this skill (ICP, journey, conversion). Then audit with this file.
- **Overlap discipline.** Visual polish, motion, and micro-interaction craft belong to other skills. Krug's unique contributions here are: **navigation clarity, copy reduction, cognitive load, the trunk test, the goodwill reservoir, and the DIY test protocol.** Don't restate polish advice as Krug.
- **The two fastest audits.** Run the **trunk test** on a random deep screen, and run the **"eliminate the question marks"** pass on every label and control. Most real friction surfaces from those two alone.
- **Simulated usability testing.** An agent can run Krug's protocol against a real product: give it one task, instruct it to narrate every hesitation, forbid it from using prior knowledge of the implementation, and log every pause, wrong click, and back-navigation. This approximates a participant, not a replacement for one — it has no genuine confusion and no domain naivety. Treat findings as hypotheses to confirm with humans, and keep Krug's filters: ignore kayak problems, discount feature requests, fix the most serious problems first.
