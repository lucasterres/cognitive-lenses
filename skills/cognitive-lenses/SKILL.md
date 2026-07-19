---
name: cognitive-lenses
description: Analyze a task through multiple independent cognitive lenses — specialized reasoning strategies such as divergent thinking, skeptical analysis, risk scanning, security, systems thinking, and empathy — then merge their observations with a consensus engine and a final self-critique pass. Use when a problem benefits from multi-perspective analysis before a final answer: design decisions, plans, research questions, code or architecture reviews, business ideas, or any task where a single-pass answer risks blind spots. Not for trivial factual lookups or tasks with one obviously correct answer.
---

# Cognitive Lenses

Give a task multiple specialized ways of thinking before producing a final answer. Each lens is a cognitive strategy or reasoning heuristic — not a persona, not a simulated person. The architecture resembles a multidisciplinary team where each expert examines the same problem from a different perspective.

Instead of `Task → Answer`, the workflow is:

```
Task → Planner → Cognitive Lenses (parallel) → Consensus Engine → Self Critique → Final Answer
```

## 1. Planner

1. Restate the task in one or two sentences to fix its scope. If the task is ambiguous in a way that changes which lenses apply, ask one short clarifying question; otherwise proceed.
2. Classify the task type (programming, research, business, creative, product/UX, operations, personal decision, or mixed) and pick lenses using [lens-selection.md](references/lens-selection.md).
3. Pick an effort tier:
   - **Light** — 3 lenses, one consensus round. Default for small or well-bounded tasks.
   - **Standard** — 4–6 lenses, one consensus round plus self-critique.
   - **Deep** — 6+ lenses, multiple consensus rounds, recursive re-invocation of lenses on unresolved conflicts. Use only when the user asks for depth or the stakes clearly justify the cost.
4. Assign each selected lens a weight from 1 (context) to 3 (decisive for this task) and state the assignments before running.

## 2. Run the lenses

The full catalog — each lens's goal, reasoning strategy, fixed questions, expected outputs, cost, recommended uses, and when *not* to use it — is in [lens-catalog.md](references/lens-catalog.md). Read it before running.

Rules of independence:

- Each lens analyzes the **original task**, not another lens's output. Lenses must not read or react to each other; convergence discovered later is evidence, engineered convergence is noise.
- Each lens answers only its own fixed questions and produces 2–5 observations. Every observation carries a confidence score (0.0–1.0) reflecting how well-supported it is by the task's actual content — never inflate confidence to win consensus.
- A lens with nothing genuinely useful to say reports "no significant findings" instead of manufacturing filler. That is a valid, valuable output.
- When running as an agent with subagent support, lenses may execute as parallel subagents (one lens per prompt, catalog entry included). When running inline, execute lenses sequentially but write each lens's section before starting the next, without revising earlier sections.

## 3. Consensus Engine

Follow [consensus-engine.md](references/consensus-engine.md). In short: cluster observations, detect agreements, conflicts, and complementary insights; rank by weight × confidence; merge duplicates; keep genuine disagreements visible instead of averaging them away.

## 4. Self Critique

One final review of the drafted answer, asking exactly:

- Did we miss something a non-selected lens would have caught? If yes and it matters, invoke that lens now (one extra round maximum in Light/Standard tier).
- Are there internal contradictions?
- Are unsupported claims being made? Strike or hedge them.
- Is the stated confidence appropriate to the evidence?

## 5. Final Answer

Present, in the user's language:

1. **Answer / recommendation** — the merged conclusion, leading with the outcome.
2. **Strongest supporting insights** — attributed to their lenses ("Security lens:", "Systems lens:"), so every conclusion is explainable back to the reasoning that produced it.
3. **Open disagreements** — conflicts that survived consensus, with both positions and what evidence would resolve them.
4. **Confidence** — one calibrated statement, with the main source of uncertainty.

Keep the final answer proportionate to the task: the lens machinery is scaffolding, not the deliverable. Do not dump raw per-lens transcripts unless the user asks for them.

## Custom lenses and extension

Users can define their own lenses. Use the template and best practices in [custom-lenses.md](references/custom-lenses.md); a new lens must fill every field of the lens structure, including "when NOT to use it", before it enters the catalog.

## Boundaries

- Lenses are reasoning strategies, never simulations of mental illnesses or imitations of real people.
- This skill structures analysis; it does not create authority. Medical, legal, and financial outputs keep all the caveats they would need without the framework, and the Medical profile in [lens-selection.md](references/lens-selection.md) is strictly non-diagnostic.
- Never fabricate lens disagreement or agreement for rhetorical effect; report what the analysis actually produced.
