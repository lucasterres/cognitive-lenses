# Latent Mode — running the lenses in the model's "subconscious"

The explicit pipeline pays 10–20× the tokens of a direct answer because every lens writes its observations out. Latent Mode asks a different question: **can the lenses shape the model's internal computation without emitting per-lens transcripts?**

## What the research actually supports

Three Anthropic findings frame what Latent Mode can and cannot promise:

1. **Models genuinely compute more than they emit.** Anthropic's circuit-tracing work ([Tracing the thoughts of a large language model](https://www.anthropic.com/research/tracing-thoughts-language-model), 2025) showed Claude planning rhyme words *before* writing a line of poetry — satisfying multiple constraints in latent activations, token-free. Internal multi-constraint processing is real, which is exactly the mechanism Latent Mode leans on: primed constraints influence the answer without being narrated.

2. **The model cannot reliably report its own internal states.** The introspection research ([Emergent introspective awareness in large language models](https://www.anthropic.com/research/introspection), 2025) found that even the most capable models detected concepts injected into their own activations only ~20% of the time under optimal conditions. Consequence: if you ask "did you really apply the Security lens internally?", the model's *yes* is not evidence. Latent execution is unverifiable by self-report.

3. **Even visible reasoning is not a faithful audit trail.** [Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think) (2025) showed models verbalizing decision-relevant factors in a minority of cases — in one experiment, Claude mentioned a hint that changed its answer only 41% of the time. This cuts both ways: it humbles the explicit mode's transcripts (they are *checkable artifacts*, not guaranteed faithful traces), and it means Latent Mode gives up less ground-truth than it first appears — but it gives up the artifacts, and artifacts are what reviews, audits, and disagreement-surfacing are built from.

**Honest summary:** Latent Mode is *priming*, not guaranteed execution. The research says latent multi-constraint computation exists (finding 1), but nobody — including the model — can confirm a specific lens ran on a specific task (findings 2 and 3).

## How Latent Mode works

Instead of one pass per lens, make **one generation pass** whose prompt has been shaped by the Planner:

1. **Planner runs normally** (it is cheap): task type, lens profile, weights, and the go/no-go decision.
2. **Prime, don't narrate.** Inject the selected lenses' fixed questions into the system prompt or prompt preamble as constraints, e.g.:

   > Before answering, silently hold these questions against the task — do not write your analysis, only let it shape the answer:
   > — What assumption in the question itself might be wrong? (Skeptical)
   > — What is the cheapest step that would produce evidence? (Scientist/Optimizer)
   > — What is the worst realistic failure and who is harmed? (Risk/Empathy)
   > — What would this look like with half the moving parts? (Minimalist)
3. **Answer format carries the residue.** Require the final answer to include: the recommendation, **one challenged premise**, **one named risk**, and **one calibrated confidence statement**. These slots force the primed computation to surface *conclusions* (cheap) without surfacing *deliberation* (expensive).
4. **Escalation hatch.** If the latent answer reveals a live conflict (e.g., the challenged premise contradicts the recommendation), escalate that single point to the explicit pipeline — one or two lenses, not the full ensemble.

With extended-thinking models, the thinking budget serves as a middle setting: lenses deliberate in thinking tokens (cheaper, discardable) and only conclusions reach the answer. The faithfulness caveat from finding 3 applies to that thinking text.

## When to use which mode

| | Explicit pipeline | Latent Mode |
|---|---|---|
| Token cost vs. direct answer | ~10–20× | ~1–2× |
| Auditability | Per-lens artifacts, attributable conclusions | Answer-level only; no trace exists |
| Disagreement surfacing | Structural (consensus engine) | Only if it survives into the answer slots |
| Verifiable execution | Yes — the transcripts exist and can be checked against the task | No — priming is not proof (introspection ≈ 20% reliable) |
| Best for | Hard-to-reverse decisions, reviews, anything a second person will audit | Medium-stakes everyday questions where a direct answer's blind spots still worry you |
| Wrong for | Trivial tasks (see poor fits) | Anything where "show your reasoning" is part of the deliverable |

Rule of thumb: **Latent Mode is a better default; the explicit pipeline is a better instrument.** Use latent for the dozens of daily medium-stakes questions, and pay for explicit when the decision is expensive, contested, or audited.

## Boundaries specific to this mode

- Never present a latent-mode answer as "reviewed by N lenses." It was *primed with* N lenses; the distinction is the whole point of findings 2–3.
- The output slots (challenged premise, named risk, confidence) are mandatory in Latent Mode — without them, priming degrades silently into an ordinary direct answer and no one can tell.
- Do not stack latent priming with persona language ("think like a paranoid hacker"). Lenses are strategies, and in latent mode the strategy text is the *only* control surface — keep it clean.
