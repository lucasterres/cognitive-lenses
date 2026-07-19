# Consensus Engine and Self Critique

Input: the per-lens observation lists, each observation carrying its lens name, text, and confidence (0.0–1.0), plus the lens weights (1–3) assigned by the Planner.

## Step 1 — Normalize and cluster

1. Flatten all observations into one list, keeping lens attribution.
2. Drop observations below 0.3 confidence unless two or more lenses independently produced the same low-confidence point (independent convergence is itself evidence — promote the merged observation and note why).
3. Cluster observations that make substantially the same point. Merging keeps the clearest wording and lists every contributing lens; a cluster's effective score is `max(weight × confidence)` across its members, plus a bump for each additional independent lens that produced it.

## Step 2 — Classify relationships

For each pair of clusters that touch the same aspect of the task:

- **Agreement** — same conclusion from different reasoning. Strongest signal in the system; these anchor the final answer.
- **Complementary** — different aspects that compose (e.g., Minimalist proposes removing a step, Risk Scanner shows the step guards a failure mode → compose into "remove the step and replace the guard with X").
- **Conflict** — incompatible recommendations. Do not average them. Apply conflict resolution below.

## Step 3 — Resolve conflicts

1. Check whether the conflict is real or a scope mismatch (one lens talking about the short term, another about the long term). Scope mismatches become complementary insights with their scopes stated.
2. If real, weigh: lens weight for this task type × observation confidence × directness of supporting evidence.
3. If one side clearly wins, adopt it and record the losing position and why it lost (explainability requirement).
4. If neither wins, **keep the disagreement visible in the final answer**, with both positions and the concrete evidence or experiment that would resolve it. A surfaced disagreement is a successful output, not a failure of the engine.

## Step 4 — Draft the unified answer

- Lead with the conclusion best supported by agreements.
- Attribute load-bearing insights to their lenses so every claim traces back to the reasoning that produced it.
- Include the surviving disagreements section.
- State one overall confidence with its dominant source of uncertainty. Calibration rule: overall confidence can never exceed the confidence of the weakest observation the conclusion depends on.

## Multiple consensus rounds (Deep tier only)

If Step 3 leaves a conflict that materially changes the recommendation, run one focused second round: re-invoke only the conflicting lenses with the specific disputed point as the task. Maximum two rounds total; after that, ship the disagreement as an open question. Never loop until artificial agreement appears.

## Self Critique (final gate)

Run on the drafted answer, answering each question explicitly:

1. **Did we miss something?** Scan the non-selected lenses in the catalog; if one would obviously have found something decisive, invoke it now (one extra invocation max outside Deep tier).
2. **Are there contradictions?** Check the answer against itself and against the surfaced disagreements.
3. **Are unsupported claims being made?** Every claim must trace to an observation or be marked as judgment.
4. **Is confidence appropriate?** Re-check the calibration rule above.
5. **Should another lens be invoked?** Only if the answer to 1 was yes; otherwise finalize.

The critique may edit, hedge, or strike — it may not add new substantive analysis of its own. New analysis belongs in a lens, where it gets confidence-scored and weighed like everything else.
