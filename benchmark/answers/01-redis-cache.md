# Task 1 — Redis cache (programming / performance)

> "Our product API is getting slow (p95 ~900 ms). Should we add a Redis cache in front of Postgres? Team of three, paid tier launches next month."

The full engine run for this task is worked in detail in [../../examples/with-vs-without.md](../../examples/with-vs-without.md); answers here are the condensed benchmark versions.

## baseline

Yes — for a read-heavy API this is the standard move. Use a managed Redis (low ops for three people), cache-aside on your hottest endpoints, TTL 60–300 s, key by endpoint + params, invalidate on writes, and track hit rate. Done carefully this usually cuts p95 dramatically and is a well-trodden path before a launch.

## latent

*Primed with: Optimizer, Minimalist, Systems, Risk, Security questions. Slots enforced.*

Probably not yet. **Challenged premise:** "slow API" doesn't establish that Postgres reads are the bottleneck — p95 alone doesn't locate it. Spend a day measuring first (`pg_stat_statements`, `EXPLAIN ANALYZE` the top queries); indexes or N+1 fixes often erase 900 ms on their own with zero new infrastructure. If measurement does point to hot, freshness-tolerant reads, add Redis *after* the launch month, not during it. **Named risk:** a new stateful dependency in launch week couples two blast radii; also key any cache by tenant, or you'll serve one customer's data to another. **Confidence:** moderate — one hour of measurement would turn this from advice into a diagnosis.

## engine

**Planner:** programming, Standard tier. Optimizer (3), Minimalist (3), Systems (2), Risk (2), Security (1). Perfectionist excluded (no artifact).

**Lens findings (condensed):** Optimizer — bottleneck asserted, never measured; hot-query fixes may be a 10× afternoon win (0.9/0.7). Minimalist — cache is the most expensive kind of complexity for 3 people; pooling/indexes/HTTP caching unexhausted (0.85). Systems — invalidation couples every write path; working cache masks query debt until an outage exposes it; stale entitlements become billing disputes post-paid-tier (0.8). Risk — stampede or Redis outage in launch week hits a Postgres unused to raw load; two risky changes share a blast radius (0.8). Security — per-tenant keying or cross-customer leakage (0.7).

**Consensus:** three lenses independently converge on "locate the bottleneck first." Optimizer-vs-Minimalist conflict resolved as sequencing, not contradiction.

**Final:** Don't add Redis yet. (1) This week: `pg_stat_statements`, top-5 queries, indexes, pgbouncer. (2) Only if measurement shows hot freshness-tolerant reads: cache after launch settles — HTTP-level before Redis. (3) If Redis lands: tenant-scoped keys, hit-rate alarms, load-test Postgres at raw traffic. Moderately confident; the read/write mix is the missing datum.
