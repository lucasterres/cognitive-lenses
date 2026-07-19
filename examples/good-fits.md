# Good fits: where the framework earns its cost

The framework pays off when a task has **blind-spot risk**: more than one dimension that matters, no single obviously-correct answer, and a real cost to getting it wrong. Each example below names the profile the Planner would pick and the specific blind spot the lenses exist to catch.

## 1. Architecture and technology decisions

> "Should we move from a monolith to microservices?" · "Postgres or DynamoDB for this workload?" · "Adopt this framework or build in-house?"

**Profile:** Programming (Systems, Minimalist, Optimizer, Risk; Historian optional).
**Why it fits:** These decisions are expensive to reverse, and the single-pass failure mode is well known — answering from the technology's popularity instead of the team's actual constraints. Historian brings precedent ("most teams that split too early regret it"), Minimalist challenges the need, Systems traces the operational consequences.

## 2. Plans about to be executed

> "Here's our migration plan for moving 40 M rows with zero downtime — review it." · "Our launch checklist for next week."

**Profile:** Operations (Risk, Perfectionist, Systems, Minimalist).
**Why it fits:** A plan is a claim about the future; Risk Scanner's pre-mortem and Perfectionist's edge-case sweep are literally designed for this shape. The with/without delta on plan reviews is usually the largest of any task type — a single-pass review tends to validate the plan's own framing.

## 3. Evaluating claims, benchmarks, and research

> "This paper says X — should we change our approach?" · "Vendor claims 4× throughput. Evaluate."

**Profile:** Research (Scientist, Skeptical, Historian, Divergent).
**Why it fits:** Claims arrive pre-framed by someone with incentives. Skeptical audits the evidence and the incentive structure; Scientist designs the cheapest decisive test instead of accepting or rejecting on vibes; Historian checks what happened to similar claims.

## 4. Product and feature decisions

> "Should we add teams/workspaces to the product?" · "Users are asking for an export button — build it?"

**Profile:** Product (UX, Empathy, Minimalist, Divergent; Entrepreneur optional).
**Why it fits:** Feature requests state a solution, not a need. Child Curiosity and Divergent recover the underlying need; Empathy finds the users the feature harms (there almost always are some); Minimalist asks what the smallest version is. Single-pass answers tend to spec the requested feature competently — the wrong deliverable done well.

## 5. Post-incident analysis

> "Here's the timeline of Saturday's outage. What should we change?"

**Profile:** Operations + Child Curiosity (5 Whys is the canonical incident tool).
**Why it fits:** Incident reviews collapse into "the fix for what broke" without structured pressure toward root causes and systemic factors. Systems Thinker finds the feedback loop that made the incident possible; Child Curiosity refuses to stop at the proximate cause.

## 6. High-stakes writing

> "Review this pricing-change announcement before it goes to 40 k customers."

**Profile:** Creative/communication (Empathy, UX-as-reader, Storytelling if installed, Risk).
**Why it fits:** The author's frame is the blind spot. Empathy reads it as the angriest affected segment will; Risk drafts the worst-faith screenshot of it; UX checks whether the one thing readers must do is findable in ten seconds.

## The common signature

A good fit has most of these:

- The decision is **hard or costly to reverse**.
- The question **spans dimensions** (technical + human + risk + cost), so no single expert view suffices.
- There's a **premise worth challenging** hiding in how the question was asked.
- Being confidently wrong is worse than being slow.
- A surfaced disagreement is itself useful output ("we can't decide X until we measure Y").

When most of these are absent, you're probably in [poor-fits.md](poor-fits.md) territory.
