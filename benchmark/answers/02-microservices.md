# Task 2 — Monolith to microservices (architecture)

> "We're five engineers, Django monolith, ~200 req/s, deploys are getting scary. Should we start splitting into microservices this quarter?"

## baseline

At your scale, probably not full microservices — but you can move toward it incrementally. Start by extracting the one or two components with the clearest boundaries (e.g., background jobs, notifications) into separate services. Invest in CI/CD, containerize, add contract tests between services, and introduce a message queue for async work. This gives you independent deploys where they hurt most without a big-bang rewrite. Revisit a broader split when the team grows.

## latent

*Primed with: Minimalist, Systems, Historian, Risk, Child-Curiosity questions. Slots enforced.*

No — and notice the question smuggles in its answer. **Challenged premise:** the stated pain is "deploys are getting scary," which is a *deployment confidence* problem, not a service-boundary problem. Five engineers at 200 req/s is comfortably monolith territory; scary deploys are usually missing tests, no staging parity, and big release batches. Fix those directly: deploy smaller and more often, add smoke tests and one-command rollback. Splitting services would give each of your five people a distributed system to operate — the historical failure mode for teams your size. **Named risk:** a quarter spent splitting is a quarter of product standstill, and you'd carry distributed-transaction complexity forever after. **Confidence:** high on the diagnosis direction, moderate on specifics — one week of measuring *why* deploys fail (list the last five scary ones) settles it.

## engine

**Planner:** architecture decision, Standard tier. Minimalist (3), Systems (2), Historian (2), Risk (2), Child Curiosity (2).

**Lens findings (condensed):** Child Curiosity (5 Whys on "deploys are scary") — scary → failures reach prod → no confidence in releases → thin tests + big batches → root need is *deploy safety*, not architecture (0.85). Minimalist — the cheapest deploy-safety fixes (CI gates, feature flags, rollback, smaller batches) need zero new services (0.85). Historian — teams under ~20 engineers that split early consistently report slower delivery and later re-consolidation; the pattern is strong (0.7). Systems — a split converts in-process calls into network failure modes owned by the same five people; on-call surface multiplies (0.8). Risk — worst case: half-migrated state at quarter end, two systems, launch-critical knowledge split (0.75).

**Consensus:** unanimous direction — treat this as a deploy-pipeline problem. No surviving conflict; Historian's precedent and Curiosity's root cause reinforce.

**Final:** Don't split this quarter. (1) Write down the last five scary deploys and what actually broke. (2) Attack those causes: CI gates, staging parity, feature flags, one-command rollback, deploy daily. (3) Extract a service later only when a boundary is forced by a real constraint (independent scaling, separate team). High confidence — the failure list in step 1 is the check.
