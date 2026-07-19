# Task 4 — Vendor benchmark claim (research / evidence)

> "A database vendor's whitepaper shows 4× the throughput of our current Postgres setup. Engineering wants to plan a migration next quarter. Should we?"

## baseline

Not on the whitepaper alone — vendor benchmarks are best-case by construction. Before planning a migration: reproduce the benchmark with your own workload (your queries, your data distribution, your hardware budget), compare at equal cost rather than equal nodes, and check the operational side — backup story, failover, ecosystem, hiring. If your reproduction still shows a large win on *your* workload and the ops story holds, then scope a migration plan; otherwise the 4× is someone else's workload.

## latent

*Primed with: Skeptical, Scientist, Historian, Risk, Optimizer questions. Slots enforced.*

Don't plan a migration; plan an experiment. **Challenged premise:** the comparison baseline is doing the heavy lifting — "4× vs. our setup" almost certainly means "vs. an untuned reference Postgres on a benchmark chosen by the vendor." Your first question isn't "is their DB fast," it's "is our Postgres slow *for our workload*, and why?" A tuning pass on your current setup is the control group the whitepaper omitted. **Named risk:** migrations are where quarters go to die — dual-write complexity, retraining, new failure modes, and an exit that's harder than the entry; meanwhile the throughput problem may be three indexes away. **Confidence:** high that the whitepaper alone justifies nothing; the two-week replay experiment (your top queries, equal hardware cost, tuned-Postgres control) produces the number that actually decides.

## engine

**Planner:** research/evidence task, Standard tier. Skeptical (3), Scientist (3), Historian (2), Risk (2), Optimizer (1).

**Lens findings (condensed):** Skeptical — vendor-authored, vendor-chosen workload, undisclosed tuning on both sides; incentive-loaded evidence; "our current setup" as baseline conflates their product with our configuration (0.9). Scientist — decisive cheap experiment: replay two weeks of production query logs on (a) candidate DB, (b) *tuned* current Postgres, equal hardware cost; pre-register the decision threshold before running (0.85). Historian — throughput-motivated migrations repeatedly find the bottleneck was schema/tuning, not engine; post-migration regret clusters around operational maturity gaps (0.7). Risk — dual-write period, data-fidelity drift, on-call for an unfamiliar system, vendor lock-in and pricing-after-adoption (0.8). Optimizer — even a true 4× only matters if throughput is the binding constraint; check current headroom first (0.75).

**Consensus:** unanimous — the claim is unusable as-is; the cheap experiment dominates. Complementary: Scientist's control group *is* Skeptical's missing baseline. No surviving conflict.

**Final:** Tell engineering: no migration planning yet — commission the two-week replay experiment with a tuned-Postgres control and a pre-agreed decision threshold (e.g., ">2.5× at equal cost on our p95-critical queries"). Simultaneously confirm throughput is actually the binding constraint. If both come back yes, *then* scope migration with the risk register above. High confidence in the process; no position on the outcome — that's what the experiment is for.
