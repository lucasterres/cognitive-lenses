# Poor fits: where the framework hurts more than it helps

A multi-lens pass costs roughly 10–20× the tokens and time of a direct answer. On the tasks below it buys nothing — or actively degrades the result. The failure mode has a name: **lens theater** — five perspectives ceremonially confirming what a one-line answer already knew.

## 1. Factual lookups and syntax questions

> "What's the Python syntax for a dict comprehension?" · "What port does Postgres use by default?"

There is one correct answer and no premise to challenge. A lens run here produces filler observations ("Security: hardcoding the port could…") that bury the answer under manufactured relevance. **Right move:** answer directly.

## 2. Emergencies and hotfixes

> "Production is down, this null check is missing, confirm the one-line fix."

Speed dominates every other dimension. The framework's value — challenging premises, surfacing second-order effects — is exactly what you don't want while the site is down. **Right move:** fix now; a *good fit* afterwards is the post-incident review ([good-fits.md](good-fits.md) §5).

## 3. Decisions already made

> "We've decided on Postgres. Write the docker-compose file."

The user asked for execution, not deliberation. Re-litigating a settled decision through Skeptical and Divergent lenses is disrespectful of the user's stated scope and wastes the entire run. **Right move:** execute; mention a concern only if execution itself reveals something material.

## 4. Matters of taste

> "Should the accent color be teal or violet?" · "Tabs or spaces for this repo?"

No experiment resolves preference, so Scientist fabricates criteria; no stakeholder is harmed, so Empathy invents some. The lenses generate confident-sounding structure around what remains a coin flip. **Right move:** state that it's preference, give one opinionated pick, move on.

## 5. Tiny reversible changes

> "Rename this variable?" · "Should this helper live in utils.py or here?"

Reversal costs less than analysis. Risk Scanner on a rename is pure theater. **Right move:** just do it — the undo button is the risk mitigation.

## 6. Tasks that are one lens, alone

> "Find security issues in this auth middleware."

The user already selected the lens. Running the other four adds noise and dilutes the security findings with Minimalist's stylistic opinions. **Right move:** run the single relevant strategy deeply, not the ensemble shallowly. (The catalog is still useful solo — each lens's fixed questions work standalone.)

## What "poor fit" looks like in practice

The same machinery from [with-vs-without.md](with-vs-without.md), applied to "What port does Postgres use?":

> **Planner:** task type unclear… selecting Perfectionist, Skeptical, Minimalist (Light tier).
> **Perfectionist:** the question omits which Postgres version… *(confidence 0.4)*
> **Skeptical:** is the user sure they mean the default? Deployments often override it… *(0.4)*
> **Minimalist:** the simplest answer is the number itself. *(0.95)*
> **Consensus:** all observations below usefulness threshold except Minimalist's.
> **Final answer:** 5432.

Twenty lines to reach four characters — and every lens *behaved correctly*. The waste was in invoking the framework at all. That's why the Planner's first duty (SKILL.md §1) is deciding **whether** to run, not just which lenses to pick.

## The heuristic

Skip the framework when **any** of these holds:

- One correct answer exists and you know where to find it.
- Undoing the action is cheaper than analyzing it.
- The user asked for execution of a settled decision.
- Time pressure dominates (restore first, analyze later).
- The task *is* a single lens — run that strategy alone instead.
