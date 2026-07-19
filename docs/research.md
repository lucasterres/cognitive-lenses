# Research grounding & further reading

Every design decision in Cognitive Lenses leans on published work. This page lists the sources, and — more useful than a bare bibliography — states **which claim in the framework each source supports or constrains**. If a source's finding is a limit, the limit is written next to it; grounding that only cites the flattering half of a paper isn't grounding.

## 1. The core: what "running lenses in the subconscious" can and cannot mean

These three Anthropic results define Latent Mode ([latent-mode.md](../skills/cognitive-lenses/references/latent-mode.md)) — the first makes it plausible, the other two bound what it may claim.

| Source | Finding | What it does for the framework |
|---|---|---|
| [Tracing the thoughts of a large language model](https://www.anthropic.com/research/tracing-thoughts-language-model) (Anthropic, 2025) | Claude plans ahead in latent activations — e.g., choosing a rhyme word before writing the line — satisfying multiple constraints without emitting tokens. | **Enables Latent Mode.** Token-free multi-constraint computation is real, so primed lens questions can shape an answer without narrated deliberation. |
| [Emergent introspective awareness in large language models](https://www.anthropic.com/research/introspection) (Anthropic, 2025) · [full paper](https://transformer-circuits.pub/2025/introspection/index.html) | Even the most capable models detected concepts injected into their own activations only ~20% of the time under optimal conditions. | **Bounds Latent Mode.** The model's claim that it "applied the lenses internally" is not evidence. Latent Mode is priming, never verified execution. |
| [Reasoning models don't always say what they think](https://www.anthropic.com/research/reasoning-models-dont-say-think) (Anthropic, 2025) | Models frequently omit decision-relevant factors from their chain-of-thought — in one setting Claude verbalized a hint that changed its answer only 41% of the time. | **Humbles Explicit Mode too.** Lens transcripts are *checkable artifacts*, not faithful introspection — which is still why the explicit pipeline is the auditable tier. |

## 2. More Anthropic interpretability & faithfulness work

- [Circuit Tracing: Revealing Computational Graphs in Language Models](https://transformer-circuits.pub/2025/attribution-graphs/methods.html) (Transformer Circuits, 2025) — the methodology behind the "tracing thoughts" results; attribution graphs over replacement models.
- [On the Biology of a Large Language Model](https://transformer-circuits.pub/2025/attribution-graphs/biology.html) (Transformer Circuits, 2025) — the case-study companion: planning in poems, multilingual circuits, motivated reasoning observed mechanistically.
- [Measuring Faithfulness in Chain-of-Thought Reasoning](https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning) (Anthropic, 2023; [arXiv:2307.13702](https://arxiv.org/abs/2307.13702)) — the earlier quantitative treatment: CoT faithfulness varies by task and *decreases* with model size on some tasks. Grounds the rule that consensus weighs observations against the task's actual content, not against how articulate a transcript sounds.
- [Persona vectors: Monitoring and controlling character traits in language models](https://www.anthropic.com/research/persona-vectors) (Anthropic, 2025) — character traits like sycophancy or hallucination-propensity are steerable directions in activation space, and persona-flavored prompting drifts them. Grounds the framework's hard rule that **lenses are strategies, never personas**: "think like a paranoid hacker" invites trait drift; "map trust boundaries and enumerate what an adversary controls" does not.

## 3. Multi-perspective reasoning in LLMs — what the ensemble borrows and where it differs

- **Chain-of-Thought prompting** — Wei et al., 2022, [arXiv:2201.11903](https://arxiv.org/abs/2201.11903). The baseline result that eliciting intermediate reasoning improves answers; every explicit lens pass is structured CoT with a fixed question set.
- **Self-Consistency** — Wang et al., 2022, [arXiv:2203.11171](https://arxiv.org/abs/2203.11171). Sampling diverse reasoning paths and aggregating beats one path. The consensus engine's "independent convergence is evidence" rule is this, applied across *strategies* instead of samples.
- **Multiagent Debate** — Du et al., 2023, [arXiv:2305.14325](https://arxiv.org/abs/2305.14325) (ICML 2024). Multiple instances critiquing each other improves factuality. Key difference: debate lets agents react to each other; Cognitive Lenses forbids inter-lens communication before consensus, precisely so convergence stays informative (see Surowiecki below).
- **Mixture-of-Agents** — J. Wang et al., 2024, [arXiv:2406.04692](https://arxiv.org/abs/2406.04692) (ICLR 2025 Spotlight). Layered LLM agents using prior-layer outputs beat single frontier models on AlpacaEval/MT-Bench. Evidence that aggregation architectures outperform single passes — and its layered cross-referencing is what our independence rule deliberately trades away for auditability.
- **Tree of Thoughts** — Yao et al., 2023, [arXiv:2305.10601](https://arxiv.org/abs/2305.10601). Deliberate exploration with backtracking; the Deep tier's recursive re-invocation on unresolved conflicts is a shallow, budgeted cousin.
- **Reflexion** — Shinn et al., 2023, [arXiv:2303.11366](https://arxiv.org/abs/2303.11366) and **Self-Refine** — Madaan et al., 2023, [arXiv:2303.17651](https://arxiv.org/abs/2303.17651). Self-feedback improves outputs; both also document its ceiling — a model reviewing itself shares its own blind spots. This is why Self Critique in this framework may edit and strike but must not add new analysis, and why it can summon a *different* lens instead.
- **Constitutional AI** — Bai et al., 2022, [arXiv:2212.08073](https://arxiv.org/abs/2212.08073). Critique-and-revise against fixed written principles; the lens catalog's fixed questions play the same role as a constitution — the critique criteria are stable text, not mood.
- **LLM-as-a-Judge (MT-Bench)** — Zheng et al., 2023, [arXiv:2306.05685](https://arxiv.org/abs/2306.05685). LLM judging correlates with human preference but carries verbosity and self-enhancement biases — the documented reason our [benchmark](../benchmark/README.md) labels itself self-judged and illustrative rather than evidence.

## 4. Cognitive-science and decision-science roots of the lenses

- **The 5 Whys** — Taiichi Ohno, *Toyota Production System* (1988). The Child Curiosity lens is this method verbatim.
- **The Pre-Mortem** — Gary Klein, ["Performing a Project Premortem"](https://hbr.org/2007/09/performing-a-project-premortem), *Harvard Business Review* (2007). The Risk Scanner's "assume it failed; reconstruct why" strategy, with evidence that prospective hindsight raises the quality of identified risks.
- **Six Thinking Hats** — Edward de Bono (1985). The closest ancestor of the whole architecture: parallel, role-separated thinking modes examining one problem. The lenses generalize the six hats into an open catalog with costs, weights, and exclusion rules.
- **Thinking, Fast and Slow** — Daniel Kahneman (2011). The System 1 / System 2 distinction is the cleanest mental model for Latent vs. Explicit mode: fast primed processing versus slow deliberate artifacts — including Kahneman's warning that System 1 confidence is not evidence, which is the calibration rule in one sentence.
- **The Wisdom of Crowds** — James Surowiecki (2004). Aggregation beats individuals only when judgments are diverse and **independent**; correlated voices produce confident error. This is the theoretical basis for the framework's strictest rule: lenses must not read each other before consensus.
- **Superforecasting** — Philip Tetlock & Dan Gardner (2015). Calibrated probabilistic judgment is a trainable skill with measurable rules (granular confidence, belief updating, premortems). Source of the consensus engine's calibration constraints.

## 5. Token economics of the two modes

Why Latent Mode is cheap and Explicit Mode is not, in mechanism rather than vibes:

- A transformer's computation per generated token is fixed; the latent planning shown in the circuit-tracing work happens *inside* that budget. Priming changes **which** internal computation happens — it does not add generated tokens. Latent Mode's only real costs are the lens questions in the prompt (input tokens, typically ~10× cheaper than output on current APIs) and the slightly longer answer forced by the mandatory slots. Measured in our micro-benchmark: ~2× the visible words of a direct answer.
- Explicit Mode pays for *generated deliberation*: every lens writes observations, consensus writes the merge, self-critique writes the review. That is 10–20× in practice, and the benchmark's condensed transcripts **under-state** it (its engine answers average ~200 words; the full worked run of the same task is ~1,200).
- Extended-thinking models sit between the modes: lens deliberation in thinking tokens is generated (billed) but discardable, and inherits the faithfulness caveat from §1.

---

*Additions welcome — especially results that would falsify a design choice here. A reference that only ever agrees with the framework isn't doing its job.*
