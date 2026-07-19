# With vs. Without: the same task, twice

One real-shaped task, answered two ways: first as a typical single-pass LLM answer, then through the Cognitive Lenses workflow. Both answers are reproduced in full so the difference is inspectable, not asserted.

## The task

> "Our product API is getting slow (p95 around 900 ms). Should we add a Redis cache in front of Postgres? We're a team of three, launching a paid tier next month."

---

## Without the framework (single-pass answer)

> Yes, adding a Redis cache is a good idea for your situation. Here's a plan:
>
> 1. Add Redis (managed, e.g. Upstash or ElastiCache, so it's low-ops for a team of three).
> 2. Cache your hottest read endpoints with a cache-aside pattern: check Redis, fall back to Postgres, store with a TTL of 60–300 s.
> 3. Key by endpoint + query params. Invalidate on writes to the affected entities.
> 4. Add cache hit-rate metrics so you can tune TTLs.
>
> This typically cuts p95 dramatically for read-heavy APIs and is a well-trodden path before your launch.

This answer is competent, actionable — and it **accepted the premise**. It never asked whether the database is actually the bottleneck, what a stale read costs once the paid tier exists, or whether the team of three can operate a new stateful dependency during a launch month.

---

## With the framework

### Planner

- **Task type:** programming (performance decision with an ops component). **Tier:** Standard.
- **Lenses and weights:** Optimizer (3), Minimalist (3), Systems Thinker (2), Risk Scanner (2), Security (1).
- Perfectionist Review excluded: there is no artifact to inspect yet ("Do NOT use when" match).

### Lens observations (independent — each lens sees only the task)

**Optimizer (weight 3)**

- No measurement is cited beyond p95. The bottleneck is asserted, not located: it could be slow queries, N+1 patterns, missing indexes, connection-pool exhaustion, or app-side serialization. *(confidence 0.9)*
- If the bottleneck is a handful of hot queries, `EXPLAIN ANALYZE` + an index can be a 10× win in an afternoon, at zero new infrastructure. *(0.7)*
- Caching has the highest ceiling **if** the workload is read-heavy with tolerant freshness needs — which the task doesn't state. *(0.6)*

**Minimalist (weight 3)**

- A cache is a new stateful system: deployment, monitoring, failure modes, invalidation code on every write path. For three people, that is the most expensive kind of complexity. *(0.85)*
- Cheaper steps not yet exhausted: indexes, query fixes, connection pooling (pgbouncer), and Postgres's own caching. *(0.8)*
- If caching does become necessary, HTTP-level caching (CDN, `Cache-Control`) on public read endpoints may need no new backend component at all. *(0.6)*

**Systems Thinker (weight 2)**

- Cache invalidation couples every write path to the cache. Each new feature now has a second correctness obligation; bugs appear as intermittent stale reads — the hardest kind to debug. *(0.8)*
- Feedback loop: a cache that works masks the underlying query debt, which keeps growing until a cache outage exposes it all at once against a database that can no longer handle raw load. *(0.7)*
- Second-order: with a paid tier, stale data stops being cosmetic — a customer seeing a stale entitlement or price is a support ticket or a billing dispute. *(0.75)*

**Risk Scanner (weight 2)**

- Worst case: cache stampede or Redis outage during launch week sends full traffic to a Postgres that hasn't handled raw load in weeks. *(0.7)*
- The change lands in the same month as the paid-tier launch — two risky changes sharing a blast radius. *(0.8)*
- New dependency = new failure domain, new on-call surface for a team with no slack. *(0.75)*

**Security (weight 1)**

- Cache keying that omits the user/tenant identity will serve one customer's data to another. This is the classic cache vulnerability and it becomes a data breach exactly when the paid tier adds per-customer data. *(0.7)*
- No other significant findings — the task has limited adversarial surface as described. *(reported, not padded)*

### Consensus Engine

- **Agreement (strongest signal):** Optimizer, Minimalist, and Systems independently converge on the same point — the bottleneck has not been located, and cheaper, less risky fixes are unexhausted. Three lenses, different reasoning, one conclusion.
- **Complementary:** Risk's "two changes share a launch blast radius" composes with Systems' "stale entitlements after paid tier" into a timing recommendation, not just a technical one.
- **Conflict (kept visible):** Optimizer holds that caching has the highest performance ceiling; Minimalist holds that it's the wrong next step. Resolution: not actually incompatible — they differ in *sequence*, not conclusion. Reframed as complementary: measure → fix queries → cache only if measurement still demands it.

### Self Critique

- Missed lens check: Empathy/UX not selected — reasonable, users only experience this as latency, which Optimizer covers. No extra invocation needed.
- Unsupported claim check: "10× win in an afternoon" is a possibility, not a promise — hedged in the final answer.
- Confidence: capped by the weakest load-bearing observation (0.6–0.7 band) → stated as "moderately confident".

### Final answer

> **Don't add Redis yet. Locate the bottleneck first — and don't ship a new stateful dependency in your launch month.**
>
> 1. **This week:** turn on `pg_stat_statements`, find the top 5 queries by total time, `EXPLAIN ANALYZE` them. Check for missing indexes and N+1 patterns. Add pgbouncer if connections are the issue. These are hours of work, no new infrastructure, and very often erase a 900 ms p95 on their own.
> 2. **If measurement shows a genuinely hot, read-heavy, freshness-tolerant path** that indexes can't fix: add caching *after* the launch settles — and consider HTTP-level caching before a Redis layer.
> 3. **If you do add Redis later:** key every entry by tenant/user (cross-customer leakage is the classic cache breach), set alarms for hit-rate collapse, and load-test Postgres at full raw traffic so a cache outage isn't a cascade.
>
> Moderately confident. Main uncertainty: your actual read/write mix and query profile — one hour of measurement resolves it and would change this from advice to a diagnosis.

---

## What the framework changed

| | Without | With |
|---|---|---|
| The premise ("cache = fix") | Accepted | Challenged by 3 independent lenses |
| Bottleneck measurement | Not mentioned | The central recommendation |
| Launch-timing risk | Not mentioned | Explicit blast-radius warning |
| Cross-tenant cache leakage | Not mentioned | Flagged before it becomes a breach |
| Stale-data cost after paid tier | Not mentioned | Second-order effect surfaced |
| Answer if caching *is* right | Same plan | Same plan — sequenced after evidence |

The single-pass answer wasn't wrong about how to cache. It was wrong about **whether to cache now** — and every insight that changed the conclusion came from a lens whose fixed questions forced it to look somewhere the direct answer didn't.

The cost: roughly 10–15× the tokens of the single-pass answer. Whether that trade is worth it is exactly what [good-fits.md](good-fits.md) and [poor-fits.md](poor-fits.md) are about.
