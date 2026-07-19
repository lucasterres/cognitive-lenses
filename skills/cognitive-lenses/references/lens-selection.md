# Adaptive Lens Selection

The Planner chooses lenses from the task type, then adjusts. Profiles below are starting points, not mandates — always apply the adjustment rules after picking a profile.

## Task-type profiles

| Task type | Core lenses | Optional additions |
|---|---|---|
| Programming | Security, Optimizer, Perfectionist Review, Systems Thinker, Minimalist | Risk Scanner (deploys/migrations), UX (developer-facing APIs) |
| Research | Scientist, Historian, Skeptical Analysis, Divergent Thinking | Systems Thinker (interconnected domains) |
| Business | Entrepreneur, Systems Thinker, Risk Scanner, Optimizer | Historian (market precedents), Empathy (customer impact) |
| Creative writing | Divergent Thinking, Empathy, UX (reader experience) | Historian (genre precedents), Minimalist (cutting) |
| Product / UX | UX, Empathy, Minimalist, Divergent Thinking | Entrepreneur (viability), Perfectionist Review (pre-launch) |
| Operations / process | Minimalist, Optimizer, Risk Scanner, Systems Thinker | Child Curiosity (inherited processes) |
| Personal decision | Child Curiosity, Risk Scanner, Empathy, Skeptical Analysis | Historian (similar past decisions) |
| Medical, non-diagnostic assistance | Scientist, Risk Scanner, Skeptical Analysis (evidence review), Empathy | — |

**Medical constraint:** the Medical profile supports understanding and preparation only. No lens combination produces diagnoses, treatment recommendations, or probability-of-disease claims; standard medical-safety boundaries apply on top of, and override, anything the lenses produce.

## Adjustment rules

1. **Cap by tier.** Light: 3 lenses. Standard: 4–6. Deep: as needed. When over the cap, drop the lowest weight × relevance lenses first.
2. **Honor exclusions.** Check every candidate's "Do NOT use when" entry in [lens-catalog.md](lens-catalog.md); an exclusion match removes the lens even if the profile lists it.
3. **Cost optimization.** When two lenses would probe the same ground (e.g., Perfectionist and Skeptical on a claims-heavy document), keep the higher-weight one in Light/Standard tier.
4. **Mixed tasks** take the union of the two nearest profiles, then re-apply the cap.
5. **User override wins.** If the user names lenses to use or skip, that overrides the profile. Note the override in the Planner output.
6. **Dependencies.** A lens that evaluates an artifact (Perfectionist, Security, UX) needs the artifact to exist; on greenfield tasks, run generative lenses (Divergent, Child Curiosity, Entrepreneur) first and evaluative lenses on the resulting draft. This is the only permitted ordering constraint — it does not create inter-lens communication.
