# Don't Make Me Think, Revisited — Steve Krug

> A short field manual for removing question marks from a screen, and for testing your own product cheaply enough that you keep doing it.

## When to reach for this

- You are about to ship a page, a signup flow, or a pricing page, and you want a pre-flight check on clarity.
- Your team argues about a design choice and nobody can win the argument with an opinion.
- Users bounce, stall in onboarding, or email you asking what the product does.
- You have no budget and no researcher, but you need real user evidence this month.
- You need a first accessibility pass and do not know where to start.

## Core thesis

- Usability means: "A person of average (or even below average) ability and experience can figure out how to use the thing to accomplish something without it being more trouble than it's worth."
- Your job is to get rid of the question marks. Every question mark adds cognitive workload.
- Users do not read pages. They scan them. Design billboards, not brochures.
- Users do not pick the best option. They satisfice: they take the first reasonable option.
- Users do not figure out how things work. They muddle through, often with wrong models.
- There is no Average User: "ALL WEB USERS ARE UNIQUE AND ALL WEB USE IS BASICALLY IDIOSYNCRATIC".
- Opinion debates about what people like are unproductive. Testing moves the team from right/wrong to works/does not work.
- Clarity is not the whole of usability. The product must also behave like a mensch: be considerate.
- Every page must be self-evident. If you cannot make it self-evident, make it self-explanatory.

## The playbook

### 1. Apply the three named laws

1. **Krug's First Law of Usability: "Don't make me think!"** It is the overriding principle, the ultimate tie breaker. If you have room in your head for only one usability rule, make this the one.
2. **Krug's Second Law of Usability: "It doesn't matter how many times I have to click, as long as each click is a mindless, unambiguous choice."** Stop counting clicks. Count thought per click. Rule of thumb: "three mindless, unambiguous clicks equal one click that requires thought."
3. **Krug's Third Law of Usability: "Get rid of half the words on each page, then get rid of half of what's left."** Removing half the words is a realistic goal. The second half is there to make you ruthless.

### 2. Kill the question marks

4. Avoid cute, clever, marketing-induced, company-specific, and unfamiliar technical names. Skew the tradeoff further toward "Obvious" than you think.
5. Make links and buttons obviously clickable. The user should never spend a millisecond deciding if a thing is clickable.
6. Remove the questions users should never have to ask: Where am I? Where should I begin? Where did they put X? What are the most important things on this page? Why did they call it that? Is that an ad or part of the site?

### 3. Design for scanning (billboard design)

7. Take advantage of conventions. Innovate when you know you have a better idea; take advantage of conventions when you don't. If you replace a convention, the replacement must either be so clear there is no learning curve, or add so much value it is worth a small one.
8. **Rule: CLARITY TRUMPS CONSISTENCY.** If you can make something significantly clearer by making it slightly inconsistent, choose clarity.
9. Create a clear visual hierarchy with three traits: the more important something is, the more prominent it is; things related logically are related visually; things are nested visually to show what is part of what.
10. Break pages into clearly defined areas. A user should be able to point at each area and name it.
11. Make it obvious what is clickable: use shape, location, and formatting. Stick to one color for all text links. Never use the same color for links and non-clickable headings.
12. Keep the noise down. The three kinds of noise are shouting, disorganization, and clutter. When editing, assume everything is visual noise (guilty until proven innocent) and remove anything not making a real contribution.
13. Format text to support scanning: use plenty of headings (more than you think, and write them carefully); make level differences between headings impossible to miss; keep paragraphs short (single-sentence paragraphs are fine); use bulleted lists, with a small amount of extra space between items; highlight key terms in bold at first appearance, but do not highlight too much.
14. **Never let headings float.** A heading must sit closer to the section it introduces than to the section it follows.

### 4. Make choices mindless

15. Prefer choices that need almost no thought, like "Animal, vegetable, or mineral?" Do not force the user to classify themselves ambiguously (for example "Home office" vs "Small business").
16. Do not show every detail of a branching decision at once. Take an initial selection to a screen that shows only the relevant follow-up.
17. When a hard choice is unavoidable, give guidance that is **brief** (the smallest amount of information that helps), **timely** (placed exactly where it is needed), and **unavoidable** (formatted so it gets noticed). Tips next to form fields, "What's this?" links, and tool tips qualify.

### 5. Cut the words

18. Kill happy talk. Test: if you hear a tiny voice saying "Blah blah blah blah blah" while you read it, it is happy talk. It conveys no useful information and says how great we are instead of what makes us great.
19. Kill instructions. Nobody reads them. Aim to eliminate them by making everything self-explanatory. Where they are unavoidable, cut them to the bare minimum. Krug's example cut a survey intro from 103 words to 34.

### 6. Navigation rules

20. "People won't use your Web site if they can't find their way around it."
21. Navigation has four purposes: find things, say where you are, tell us what's here (navigation reveals content), tell us how to use the site, and give confidence in the people who built it.
22. Use **persistent navigation** on every page: Site ID, Sections, Utilities, and Search. Same place, same look, everywhere. One exception: on form pages, use a minimal version with the Site ID, a link to Home, and any Utilities that help fill the form.
23. Put the Site ID at the top, in or near the upper-left corner. It frames the page. It should look like a brand logo and be recognizable at any size. Almost all users expect the Site ID to link Home.
24. Sections are the primary navigation: the top level of the hierarchy. Secondary navigation lists the subsections of the current section.
25. Utilities are links outside the content hierarchy (Sign in, Help, Site Map, Cart, About Us, Contact Us). Make them slightly less prominent than the Sections. The persistent navigation holds only four or five Utilities. Push the rest into the footer.
26. Keep a Home button or link in sight at all times. It is the reset button.
27. Search: a box, a button, and either the word "Search" or the magnifying glass icon. Use the word "Search", not Find, Quick Find, Quick Search, or Keyword Search. If the box is labeled "Search", label the button "Go". Add no instructions. Add no scope options up front; offer scoping on the results page, when the user actually needs it. Spell out the scope only if there is real possible confusion.
28. Design the third level and below. Most sites break down after level two. Produce sample pages showing navigation for all potential levels before arguing about the color scheme.
29. Page names are the street signs of the Web. Four rules: every page needs a name; the name must frame the content unique to that page; the name must be prominent (usually the largest text on the page); **"The name of the page will match the words I clicked to get there."** If exact match is impossible, match as closely as possible and make the reason for the difference obvious.
30. Show "You are here" by highlighting the current location in every nav bar, list, and menu. The common failing is that the indicator is too subtle. Apply more than one visual distinction, for example a different color plus bold. General rule for designers: if you think a visual cue sticks out like a sore thumb, make it twice as prominent.
31. Breadcrumbs: put them at the top; use ">" between levels; boldface the last item, which is the current page and is not a link. Most useful in a large site with a deep hierarchy.
32. Tabs work because they are self-evident, hard to miss, and slick. If you use them, the active tab must be a different color or shade and must physically connect with the space below it, so it pops to the front.

### 7. The trunk test (named test)

33. Run it on any page: imagine you were blindfolded, locked in a car trunk, driven around, and dumped on a page deep inside the site. With vision still blurry, you should answer without hesitation: What site is this? (Site ID) What page am I on? (Page name) What are the major sections of this site? (Sections) What are my options at this level? (Local navigation) Where am I in the scheme of things? ("You are here" indicators) How can I search?
34. Procedure: **Step 1:** choose a page anywhere in the site at random, and print it. **Step 2:** hold it at arm's length or squint so you cannot study it closely. **Step 3:** as quickly as possible, find and circle: Site ID, Page name, Sections (primary navigation), Local navigation, "You are here" indicators, Search. Then ask friends to try it too.

### 8. Home page rules

35. The Home page must carry: site identity and mission, site hierarchy, search, teases (content promos and feature promos), timely content, deals, shortcuts, and registration/sign-in. It must also show me what I'm looking for, expose me to what I'm not looking for, show me where to start, and establish credibility and trust.
36. **The Big Bang Theory of Web Design:** the first few seconds on a new site or page are critical. Initial impressions predict later, more reasoned assessments. If people are lost when they start out, they usually just keep getting loster.
37. The thing that gets lost in Home page compromises, and the one you cannot afford to lose, is the big picture: what the site is. Nobody inside the organization will notice that the main point is missing. So it is one of the most important things to test with outsiders.
38. Get the message across in three places: the **tagline** next to the Site ID, the **Welcome blurb** (a terse description in a prominent block, usually top left or center), and the **"Learn more"** (a short explanatory video).
39. Tagline rules: clear and informative; explains exactly what the site or organization does; six to eight words; conveys differentiation and a clear benefit. Nielsen's test, which Krug endorses: a really good tagline is one that no one else in the world could use except you. Bad taglines sound generic. Do not confuse a tagline with a motto: a motto expresses a guiding principle, a tagline conveys a value proposition.
40. Never use a corporate mission statement as a Welcome blurb. Nobody reads them.
41. Use as much space as necessary to explain a novel proposition, and no more. Do not mention every feature, only a few of the most important.
42. Answer the fifth question: where do I start? After a quick look the visitor should be able to say: here's where to start if I want to search; here's where to start if I want to browse; here's where to start if I want to sample their best stuff. Make entry points look like entry points and label them clearly ("Search", "Browse by Category", "Sign in", "Start here").
43. Guard against Home page promotional overload. It is a tragedy of the commons: "Any shared resource (a 'commons') will inevitably be destroyed by overuse." Educate stakeholders and offer alternatives: cross-promote from other popular pages, or take turns using the same space.
44. Deep links matter now, but people still bounce up to the Home page to get their bearings. So every page should orient the visitor, and the Home page must still do this job well.

### 9. Mobile rules

45. The basic principles do not change on mobile. People move faster and read even less.
46. Most serious usability problems are the result of a poor decision about a tradeoff. Mobile is mostly a tradeoff problem.
47. Mobile First is useful because it forces you to determine what is really essential. Do not use it to decide what to include based on what people supposedly do "on the move": people use phones on the couch and expect to do everything.
48. If you include everything, prioritize harder. Frequent or urgent things stay close at hand. Everything else can be a few taps away, with an obvious path.
49. More taps and more scrolling are acceptable on small screens, as long as the user stays confident that what they want is further down or behind that button.
50. **MANAGING REAL ESTATE CHALLENGES SHOULDN'T BE DONE AT THE COST OF USABILITY.**
51. Scalable design (responsive, adaptive, fluid) is a lot of work and very hard to do well, but it is no longer optional. Avoid maintaining two separate versions.
52. Three minimum mobile courtesies: allow zooming; do not dump a deep link on the mobile Home page ("Don't leave me standing at the front door"); always provide a link to the full site (the convention is a Mobile Site / Full Site toggle at the bottom of every page).
53. Protect affordances: the visual clues that suggest how to use a thing. "By definition, affordances are the last thing you should hide." They do not all have to hit you in the face, but they must be visible enough for people to notice the ones they need.
54. Touch screens have no cursor, so no hover. Tool tips, hover color changes, and hover-revealed menus do not exist for mobile users. Find replacements.
55. Flat design removes visual distinctions and takes useful information with the decoration. If you use it, use all the remaining dimensions to compensate for what you lose.
56. Speed matters most on mobile. Slow performance equals frustration for users and loss of goodwill for publishers. Mobile download speeds are unreliable. Do not let responsive solutions ship code and images larger than the screen needs.
57. For apps, target learnability and memorability. A first-run tour is not enough if help cannot be found again. If it is easy to learn the first time, it is easy to learn the second time. Delight is the extra credit assignment: pursue it, but do not let it cost usability.

### 10. Be a mensch (goodwill)

58. Assume every visitor starts with a reservoir of goodwill. Each problem lowers it. It is idiosyncratic, it is situational, you can refill it, and sometimes a single mistake empties it (for example, a registration form with tons of fields).
59. Things that diminish goodwill: hiding information the user wants (support phone numbers, shipping rates, prices); punishing me for not doing things your way (rejecting spaces in a credit card number); asking for information you do not need; shucking and jiving me with faux sincerity; putting sizzle in my way (feel-good marketing photos); looking amateurish.
60. Things that increase goodwill: know the main things people want to do and make them obvious and easy; tell me what I want to know, including the things you would rather not say; save me steps; put effort into it; know what questions I am likely to have and answer them in real, current, candid FAQs; provide creature comforts like printer-friendly pages; make it easy to recover from errors; when in doubt, apologize.
61. If you deliberately do a user-unfriendly thing for revenue, do it as an informed business decision, not inadvertently.

### 11. Accessibility guidance

62. You cannot call a product usable unless it is accessible, unless you decide that people with disabilities are not part of your audience.
63. Krug's **three-second accessibility test**: increase the size of the type. Sites that have moved beyond fixed-size fonts respond to Text Size; almost every site fails.
64. The reason that matters: it is the right thing to do. And expect a legislative stick sooner or later.
65. **#1. Fix the usability problems that confuse everyone.** What confuses most people will almost certainly confuse users with accessibility issues, and they will have a harder time recovering. Test often and smooth out the confusion first. Fixing code without fixing clarity does not work.
66. **#2. Read an article:** Theofanos and Redish, "Guidelines for Accessible and Usable Web Sites: Observing Users Who Work with Screen Readers." Key finding: screen-reader users scan with their ears. They listen to the first few words of a link or line, then move on. A keyword that is not at the beginning of a link or line may never be heard.
67. **#3. Read a book:** A Web for Everyone by Sarah Horton and Whitney Quesenbery; Web Accessibility: Web Standards and Regulatory Compliance by Jim Thatcher et al.
68. **#4. Go for the low-hanging fruit:** add appropriate alt text to every image, and an empty (null) alt attribute for images screen readers should ignore; use headings correctly (h1 for the page title or main content heading, h2 for major sections, h3 for subheadings, then style with CSS); make forms work with screen readers by using the HTML label element to associate fields with their labels; put a "Skip to Main Content" link at the beginning of each page; make all content accessible by keyboard; create significant contrast between text and background; use an accessible template. Learn the details at webaim.org.

### 12. The four definitive answers

69. Don't use small, low-contrast type.
70. Don't put labels inside form fields, unless the form is exceptionally simple, the labels disappear on typing and reappear if the field is emptied, the labels can never be confused with answers, there is no chance of submitting the label along with the input, and they are completely accessible.
71. Preserve the distinction between visited and unvisited text links. Any colors are fine as long as they are noticeably different.
72. Don't float headings between paragraphs.

## The usability test protocol

**Cadence.** One morning a month. In a morning you test three users, then debrief over lunch. When you leave the debriefing, the team has decided what to fix before the next round, and testing is done for the month. On Agile, test more often, for example two users every two weeks. Pick a fixed day, such as the third Thursday, and keep it. Do not tie testing to milestones, because schedules slip and testing slips with them.

**Why three participants.** The purpose is not to prove anything, and not to find all the problems. It is a qualitative method: give tasks, observe, learn, get actionable insights. "You can find more problems in half a day than you can fix in a month." Three users are very likely to hit many of the most significant problems for the tasks you test. More rounds beat wringing everything out of one round. "Testing one user is 100 percent better than testing none." "Testing one user early in the project is better than testing 50 near the end."

**Cost.** A traditional lab study cost $20,000 to $50,000 per shot. Nielsen's 1989 "discount usability" brought it to $5,000 to $10,000 per round. Do-it-yourself testing is for when you have no time and no money. Typical participant incentive for a one-hour session: $50 to $100 for average Web users, up to several hundred dollars for busy, highly paid professionals. Krug offers a little more than the going rate. If you have any money for testing, spend it on the best snacks you can, to lure observers in.

**Recruiting.** **RECRUIT LOOSELY AND GRADE ON A CURVE.** Try to find users who reflect your audience, but do not get hung up on it. Loosen the requirements, then make allowances: when someone has a problem, ask "Would our users have that problem, or was it only a problem because they didn't know what our users know?" If your product needs domain knowledge, recruit some people who have it, but not all. Always include some participants outside the target audience: it is a bad idea to design so only your target audience can use it; we are all beginners under the skin; and experts are rarely insulted by something clear enough for beginners. Sources: user groups, trade shows, Craigslist, Facebook, Twitter, customer forums, a pop-up on your site, friends and neighbors. Krug points to the Nielsen Norman Group's free 147-page report How to Recruit Participants for Usability Studies.

**Room and kit.** A quiet room with a table and two chairs. A computer with Internet access, a mouse, a keyboard, and a microphone. Screen sharing software (GoToMeeting, WebEx) so observers watch from another room. Screen recording software (Camtasia) for the record. Observation room: a computer with Internet access and screen sharing, a large monitor or projector, and external speakers.

**Facilitator.** Almost anyone can facilitate. Choose someone patient, calm, empathetic, and a good listener. Not the office crank. The facilitator's main job, beyond keeping the participant comfortable and focused, is to encourage thinking out loud.

**Observers.** As many as possible: team members, stakeholders, managers, executives. During the break after each session, every observer writes down the three most serious problems they saw in that session.

**What and when to test.** Start as early as possible and keep testing through the whole process. Before you design anything, test competitive sites with three participants. If you are redesigning, test the current version first, so you know what is broken and what works and must not be broken. Then test everything the team produces: rough sketches, wireframes, page comps, prototypes, live pages.

**Choosing tasks.** List the things people need to be able to do with what you are testing. Example for a login prototype: create an account; log in using an existing username and password; retrieve a forgotten password; retrieve a forgotten username; change answer to a security question. Choose enough tasks to fill about 35 minutes of a one-hour test. Word each task carefully and include information the participant needs but would not have, such as demo login details. Krug's example wording:

```
You have an existing account with the username delphi21 and the password
correcthorsebatterystaple. You've always used the same answers to security questions on every
site, and you just read that this is a bad idea. Change your answer for this account.
```

Let participants choose some details of the task. "Find a book you want to buy, or a book you bought recently" beats "Find a cookbook for under $14": it raises emotional investment and lets them use their own knowledge.

**One-hour session structure.**
- Welcome, 4 minutes: explain how the test works.
- The questions, 2 minutes: a few questions about the participant, to relax them and gauge how Web-savvy they are.
- The Home page tour, 3 minutes: open the Home page and ask what they make of it.
- The tasks, 35 minutes: watch them work and keep them thinking aloud. If they go quiet, prompt with "What are you thinking?", "What are you looking at?", "What are you doing now?". Do not ask leading questions. Do not help unless they are hopelessly stuck or extremely frustrated. If they ask for help, say "What would you do if I wasn't here?".
- Probing, 5 minutes: ask about anything that happened, including questions from the observation room.
- Wrapping up, 5 minutes: thank them, pay them, show them to the door.

**The script.** Krug's script is at rocketsurgerymadeeasy.com, along with a sample recording permission form. Read your lines exactly as written; the wording has been carefully chosen. The introduction, verbatim from the book:

```
Hi, Janice. My name is Steve Krug, and I'm going to be walking you through this session. Before
we begin, I have some information for you, and I'm going to read it to make sure I cover
everything.
You probably already have a good idea of why we've asked you to come here today, but let me
go over it again briefly. We're testing a Web site that we're working on so we can see what it's
like for people to use it. The session should take about an hour.
I want to make it clear right away that we're testing the site, not you. You can't do anything
wrong here. In fact, this is probably the one place today where you don't have to worry about
making mistakes.
We want to hear exactly what you think, so please don't worry that you're going to hurt our
feelings. We want to improve it, so we need to know honestly what you think.
As we go along, I'm going to ask you to think out loud, to tell me what's going through your
mind. This will help us.
If you have questions, just ask. I may not be able to answer them right away, since we're
interested in how people do when they don't have someone sitting next to them to help, but I will
try to answer any questions you still have when we're done.
And if you need to take a break at any point, just let me know.
You may have noticed the microphone. With your permission, we're going to record what
happens on the screen and what you say. The recording will be used only to help us figure out
how to improve the site, and it won't be seen by anyone except the people working on the
project. It also helps me, because I don't have to take as many notes.
Also, there are a few people from the Web design team observing the session in another room.
(They can't see us, just the screen.)
If you would, I'm going to ask you to sign a simple permission form for us. It just says that we
have your permission to record you, but that it will only be seen by the people working on the
project.
Do you have any questions before we begin?
```

The Home page tour lines, verbatim:

```
First, I'm just going to ask you to look at this page and tell me what you make of it: what strikes
you about it, whose site you think it is, what you can do here, and what it's for. Just look around
and do a little narrative.
You can scroll if you want to, but don't click on anything yet.
```

Before this point, keep the browser open to something neutral, such as Google, so there is nothing distracting to look at. Then open a tab with the site and give the participant the mouse.

Krug also gives the background-question openers, verbatim: "Before we look at the site, I'd like to ask you just a few quick questions. First, what's your occupation? What do you do all day?" and "Now, roughly how many hours a week would you say you spend using the Internet, including Web browsing and email? Just a ballpark estimate." Accurate answers do not matter. The point is to get them talking and to show that you are listening. Do not hesitate to admit ignorance. Your role is not expert; it is good listener.

Task hand-off lines, verbatim: "OK, now we're going to try doing some specific tasks." "And again, as much as possible, it will help us if you can try to think out loud as you go along." When a participant hesitates between options: "Well, which one do you think you'd click on?" then "Why don't you go ahead and do it?" Let each task run until (a) they finish, (b) they get really frustrated, or (c) you are not learning anything new by watching them muddle through.

**Typical problems you will see.** Users are unclear on the concept. The words they are looking for are not there. There is too much going on, so what they need does not pop out of the visual hierarchy.

**The debriefing: how to pick what to fix.** Debrief over lunch right after the tests, while it is fresh. **FOCUS RUTHLESSLY ON FIXING THE MOST SERIOUS PROBLEMS FIRST.**
1. Make a collective list. Go around the room; each person names the three most serious problems they observed, out of the nine they wrote down (three per session). Write them on a whiteboard. Track "me too" with checkmarks. No discussion yet. Problems must be observed problems, things that actually happened in a session.
2. Choose the ten most serious problems. Informal voting works; start with the most checkmarks.
3. Rate them 1 to 10, with 1 the worst. Copy them to a new list, worst at the top, with space between them.
4. Create an ordered list. From the top, write a rough idea of how you will fix each one in the next month, who does it, and what resources it needs.
5. You do not have to fix each problem perfectly. Do something, often just a tweak, that takes it out of the "serious problem" category.
6. When you have allocated all the time and resources you have for the next month, STOP. The group has decided and committed.

**Fix-selection heuristics.** Keep a separate list of low-hanging fruit: things one person can fix in under an hour without permission from anyone outside the debriefing. Resist the impulse to add things: the right fix is often to take away what obscures the meaning, not to add an explanation. Take "new feature" requests with a grain of salt: ask the participant during probing to describe how the feature would work, and they usually talk themselves out of it. Participants are not designers; when they do have a great idea you will know immediately, because your first thought will be "Why didn't we think of that?!" Ignore "kayak" problems: if everyone who hits it notices quickly, recovers without help, and is not fazed, let it go. In general, if the user's second guess about where to find things is always right, that is good enough.

**Variants.** Remote testing over screen sharing removes travel and expands the pool from "people near your office" to "almost anyone"; participants need high-speed Internet and a microphone. Unmoderated remote testing (UserTesting.com) records people doing your tasks; you send tasks and a link and watch a video, often within an hour. You lose real-time interaction, but it is inexpensive and needs almost no effort.

**Mobile testing.** The process is identical; the difference is logistics. Krug's recommendations: use a camera pointed at the screen instead of mirroring, so observers see gestures and taps; attach the camera to the device so the participant can hold it naturally; do not bother with a camera pointed at the participant's face. Setup: connect the camera to the facilitator's laptop by USB, display it with AmCap (PC) or QuickTime Player (Mac), share that laptop screen with observers, and run the screen recorder on the observation room computer. Krug's own rig ("Brundlefly") was a webcam clipped to a book-light gooseneck, about $30 in parts and an hour to build.

**Selling it internally.** Get your boss, and her boss, to watch one test in person; live beats a recap. If they will not come, use clips under three minutes. Do the first test on your own time, without asking permission, with volunteer participants, and pick a target with one serious problem you can fix quickly, then fix it and publicize it. Test the competition: everyone loves it and nobody's own work is on the line.

## Rules and heuristics

| Rule | Why | Failure mode if ignored |
| --- | --- | --- |
| Don't make me think | Every question mark adds cognitive workload and drains attention from the task | Users puzzle, lose confidence in you, and leave |
| Self-evident, or at least self-explanatory | Pages must work at a glance | Users misread the page and force-fit wrong assumptions onto everything after |
| Clicks may be many if each is mindless | What costs the user is thought and uncertainty, not clicks | Short paths that require hard choices still stall the user |
| Get rid of half the words, then half of what's left | Nobody reads the extra words, and they make pages look daunting | Noise hides the useful content and pages need scrolling |
| Follow conventions unless you have a better idea | Conventions need no explanation | Users have to relearn basics on your product |
| Clarity trumps consistency | Consistency is a means, clarity is the goal | You defend a confusing pattern because it matches the rest |
| Clear visual hierarchy | It preprocesses the page for the user | Everything looks equally important, so the user scans word by word |
| Make it obvious what's clickable | Users are looking for the next thing to click | Dead taps, missed links, lost trust |
| Everything is visual noise until proven innocent | Attention and time are limited | Low signal-to-noise ratio; the message is buried |
| Never let headings float | Position tells the reader what the heading belongs to | Readers attach the heading to the wrong section |
| Guidance must be brief, timely, unavoidable | Help is only useful at the moment of the decision | Help exists but nobody reads it or finds it |
| Persistent navigation on every page | Constant confirmation of where you are and how things work | Users get lost and cannot tell they are still on your site |
| The page name matches what I clicked | It is an implicit social contract | Every mismatch costs a beat of thought and some trust |
| Make "You are here" twice as prominent as feels right | Users are in a hurry and miss subtle cues | The indicator becomes noise instead of a cue |
| Say what the product is, on the Home page, in the tagline | Nobody inside the company notices the main point is missing | Visitors cannot tell what you sell |
| Tagline: six to eight words, differentiating, no one else could use it | It is where users expect the value proposition | Generic slogan that says nothing |
| Prioritize hard on small screens | Space is scarce, but users want everything | A crippled mobile version, or a cluttered one |
| Managing real estate should not cost usability | The screen is a constraint, not an excuse | Tiny targets, hidden affordances, unreadable text |
| Do not hide affordances | Affordances are the signal that a thing is usable | Users cannot tell what is interactive, worse without hover |
| Speed is a usability feature | Slow equals frustration and lost goodwill | Users form the habit of using a competitor |
| Behave like a mensch | Goodwill is a limited reservoir | One bad moment empties it, and they tell others |
| Fix the confusion for everyone first | Confusion is worse for users who cannot see the page | Accessibility code fixes on top of an unclear product |
| Recruit loosely and grade on a curve | Perfect recruiting means less testing | Testing keeps getting postponed |
| Focus ruthlessly on the most serious problems first | You always find more than you can fix | You ship low-hanging fruit and keep the serious defects |
| A morning a month | Simple enough that you keep doing it | Testing becomes a big deal, so it happens too late |

## Anti-patterns

| Anti-pattern | What it looks like | Fix |
| --- | --- | --- |
| Cute or internal naming | "Job-o-Rama" instead of "Jobs" | Skew names toward obvious, further than feels comfortable |
| Happy talk | "Welcome to..." paragraphs that say how great you are | Delete it; state what the thing is and what it does |
| Instruction dumps | A wall of text at the top of a form or survey | Make it self-explanatory; if unavoidable, cut to the minimum |
| Ambiguous self-classification | "Home office" vs "Small business" as the first choice | Remove the choice, or defer detail to a second screen |
| Shouting | Exclamation points, many typefaces, bright colors, slideshows, pop-ups | Decide what is actually most important and build a hierarchy |
| Disorganization | Elements strewn about with no alignment | Use a grid |
| Clutter | A Home page with too much stuff | Delete anything not making a real contribution |
| Floating headings | Heading sits midway between two blocks | Move it closer to the section it introduces |
| Wall of words | Long unbroken paragraphs | Split paragraphs; use headings and bulleted lists |
| Subtle visual cues | A "You are here" state a designer can see and a user cannot | Apply two distinctions at once; double the prominence |
| Fancy search wording | "Quick Find", "Keyword Search", "Type a keyword" | Box, button, the word "Search" or the magnifier; label the button "Go" |
| Search scope options up front | Dropdowns to limit the search before searching | Offer scoping on the results page |
| Ad hoc lower-level navigation | Levels three and below invented per page | Design sample pages for every level before styling |
| Link and page name mismatch | Click "Hot mashed potatoes", land on "Recipes" | Match the wording, or make the reason for the difference obvious |
| Mission statement as Welcome blurb | "XYZCorp offers world-class solutions in the burgeoning field of..." | Write a concrete tagline and a terse Welcome blurb |
| Motto instead of tagline | "We bring good things to life" | Write a value proposition, not an ideal |
| Home page promo overload | Every stakeholder gets a box above the fold | Cross-promote elsewhere, rotate the same slot, protect the commons |
| Deep link dumped on the mobile Home page | Tap an emailed link, land on the mobile front door | Send the link to the actual content |
| No zoom allowed | Tiny fixed text you cannot pinch | Allow zooming; better, make the site responsive |
| Flat design with no distinctions | Buttons and labels look identical | Use the remaining dimensions to restore the signal |
| Hover-dependent interface on touch | Tool tips and hover menus | Replace with always-visible affordances |
| Loading everything before the thing I asked for | Tap an alert, wait for unrelated photos | Load what the user asked for first |
| Hidden support number, shipping cost, or price | Cost revealed three pages in | State it up front; keep the number visible |
| Formatting punishment | Credit card field rejects spaces | Accept what the user types and normalize it in code |
| Over-asking on forms | Fields you do not need for this task | Ask only for what the task requires |
| Faux sincerity | "Your call is important to us" | Say something true, or say nothing |
| Sizzle in the way | Feel-good marketing photos before the content | Get to the point |
| Marketing FAQs | Questions We Wish People Would Ask | Publish the actual top five questions from support, candidly |
| Labels inside form fields | Placeholder text as the only label | Use real labels outside the field |
| Visited links styled like unvisited | One link color for everything | Keep the visited state noticeably different |
| Small, low-contrast type | Light grey 11px body text | Bigger, or higher contrast, ideally both |
| Focus group in place of a usability test | People at a table discussing opinions about the product | Watch one person at a time try to use it |
| Testing to settle an aesthetic argument | "Sexy design vs elegant design, let's test it" | Test the value proposition and the tasks first |
| Dark patterns | Pre-checked newsletter box, fake "Start Download" buttons, bundled toolbars | Refuse; it is not part of your job |

## Quotes worth keeping

1. "Don't make me think!" — Use when a design decision is deadlocked; it is the ultimate tie breaker.
2. "It doesn't matter how many times I have to click, as long as each click is a mindless, unambiguous choice." — Use when someone demands a three-click rule.
3. "Get rid of half the words on each page, then get rid of half of what's left." — Use on any landing page or onboarding copy review.
4. "If you can't make something self-evident, you at least need to make it self-explanatory." — Use when the feature is genuinely novel and cannot be obvious.
5. "We're thinking 'great literature' (or at least 'product brochure'), while the user's reality is much closer to 'billboard going by at 60 miles an hour.'" — Use to reset the team's mental model of the reader.
6. "If your audience is going to act like you're designing billboards, then design great billboards." — Use when someone laments that users do not read.
7. "CLARITY TRUMPS CONSISTENCY" — Use when a design system rule is making a screen worse.
8. "ALL WEB USERS ARE UNIQUE AND ALL WEB USE IS BASICALLY IDIOSYNCRATIC" — Use when a persona or an "average user" claim is being used to win an argument.
9. "Testing one user is 100 percent better than testing none." — Use when you have almost no time and are tempted to skip testing.
10. "You can find more problems in half a day than you can fix in a month." — Use to justify prioritizing instead of listing.
11. "FOCUS RUTHLESSLY ON FIXING THE MOST SERIOUS PROBLEMS FIRST" — Use at the debriefing, when the team drifts to low-hanging fruit.
12. "RECRUIT LOOSELY AND GRADE ON A CURVE" — Use when recruiting perfectionism is delaying a test.

## Applies to

- **Idea validation.** Krug draws a hard line: focus groups and market research answer whether you are building the right product and whether it is desirable; usability tests answer whether people can use what you built. Use focus groups in the planning stage, usability tests throughout. Also: test competitors with three participants before you design anything.
- **Positioning.** The tagline rules are positioning rules. Six to eight words, differentiating, a clear benefit, and one that no one else in the world could use except you. A motto is not positioning. Nobody inside the company will notice the main point is missing, so test the Home page with outsiders.
- **Landing page / CRO.** Almost the whole book applies: billboard design, visual hierarchy, one obvious entry point per intent, kill happy talk, cut half the words, answer "what is this" in the tagline, the Welcome blurb, and a "Learn more" video for a novel proposition. Krug also treats hidden pricing as a goodwill leak.
- **Onboarding / activation.** Make each choice mindless; do not front-load a hard self-classification; give guidance that is brief, timely, and unavoidable. Apps need to be learnable and memorable: a first-run tour that cannot be found again is not enough. His Clear app test is the cautionary case: nobody completed the primary task after the tour and the tutorial.
- **Retention / churn.** The reservoir of goodwill is the retention model. Speed, candor, error recovery, saved steps, and real FAQs refill it. Memorability decides whether people come back to an app: "if you have to invest the same effort the next time... there's a good chance you'll abandon it." Also: "You can get away with a site that people muddle through only until someone builds one down the street that makes them feel smart."
- **Product decisions.** Replace opinion debates with tests. The right question is not "do most people like pull-downs" but "does this pull-down, with these items and this wording in this context on this page create a good experience for most people who are likely to use this site?" Also: most serious usability problems come from a poor decision about a tradeoff, so name your constraints explicitly.
- **Growth.** Only indirectly, and mostly as a warning. Krug tells you to refuse manipulation work: pre-checked opt-ins, fake download buttons, bundled toolbars. He accepts influence and persuasion that is not deceptive, and points to Cialdini for that.

Not covered: pricing. The book says nothing about how to price. It only says that hiding prices costs goodwill, and that price disclosure should be up front.

## Conflicts and limits

- The book is from 2014 and its technology advice has aged. The named tools are dated: GoToMeeting, WebEx, Camtasia, AmCap, Dreamweaver, WordPress themes, and Krug's claim that mobile screen recording and screen sharing do not exist yet. That last one is now false; modern phones record and mirror natively, so the Brundlefly camera rig is a historical curiosity, though his reason for wanting to see fingers still holds.
- Flat design is discussed as a current trend that "may have waned by the time you read this." Treat the underlying point (do not remove the signal with the decoration) as durable and the trend commentary as dated.
- The Mobile Site / Full Site toggle at the bottom of every page is described as "the current convention." It is no longer a common pattern.
- Responsive design is described as unsettled and very hard. That has largely been solved by tooling since publication.
- The accessibility chapter is a starting point, not a standard. It does not mention WCAG levels, ARIA, focus management, motion sensitivity, or automated CI checks. The cited Theofanos and Redish article was already ten years old at publication. The Nielsen Norman recruiting report is from 2003.
- Krug is explicit that he offers no hard and fast rules; the honest answer to most usability questions is "It depends." He also gives no numeric thresholds: no contrast ratios, no font sizes, no load-time budgets.
- Participant incentive figures ($50 to $100) are 2014 US dollars and are low today.
- The three-participant number is contested by people who want statistical confidence. Krug concedes the criticism is true and argues it does not matter for a qualitative method. If you need proof rather than insight, this protocol is the wrong tool.
- Krug says usability tests cannot measure desirability, and that desirability is a market research question. That boundary is contested in current practice.
- The book is web-page centric. It does not cover application state, data-heavy dashboards, multi-step workflows in complex SaaS, notifications, or search relevance. It says almost nothing about quantitative product analytics.
- **Source text defects.** The extraction has no images, and the book leans on figures. Several enumerated lists therefore have no content in the text: the four elements of persistent navigation, the four questions the Home page must answer, the three search-box patterns, the ways to mark the current location, the "Top Four Plausible Excuses for not Spelling Out the Big Picture," the "Top Five Plausible Reasons for not Testing Web Sites," the accessibility reasons list, and the before/after code and page examples. Figure captions appear as stray lines. The Chapter 5 title renders as "Omit                words," which is the book's visual joke about striking out "needless." The alt attribute example is mangled as `<alt="">`. One in-book cross-reference reads "I know I mentioned this is Chapter 3" (a typo for "in"). Page-number references in the index are to the print edition and cannot be verified from this text.
