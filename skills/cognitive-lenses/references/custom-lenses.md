# Custom Lenses — Template and Best Practices

The framework is extensible: any number of custom lenses may be added. A custom lens is a markdown entry in the same structure as [lens-catalog.md](lens-catalog.md); project-specific lenses live in the project (e.g., a `lenses/` folder or an appendix to a copy of the catalog) and are loaded by the Planner alongside the built-ins.

## Template

```markdown
## <Lens Name>

- **Description:** <the kind of thinking it contributes, one sentence>
- **Goal:** <the single outcome it optimizes for>
- **Reasoning strategy:** <how it works through a task, 1–3 sentences>
- **Fixed questions:**
  - <question 1>
  - <question 2>
  - <question 3>
- **Expected outputs:** <shape and size of its observations>
- **Cost:** <Low | Medium | High>
- **Recommended for:** <task types where it earns its cost>
- **Do NOT use when:** <REQUIRED — where it wastes effort or degrades answers>
```

Every field is required. A lens without a real "Do NOT use when" entry is not done — a lens applicable everywhere is a lens sharpened nowhere.

## Design rules

1. **One strategy per lens.** If the description needs "and", split it. Overlapping lenses produce duplicate observations that inflate false consensus.
2. **Strategies, not personas.** "Accessibility Lens" (checks WCAG-style barriers) is a lens; "Grumpy Senior Dev" is a persona — the strategy hiding inside it should be extracted and named. Never model a lens on mental illnesses or on real, identifiable people.
3. **Fixed questions must be answerable from the task.** Questions requiring information the lens can't have ("what will the market do next year?") produce confident fabrication.
4. **Declare honest cost.** The Planner drops lenses on cost; an underdeclared cost cheats the selection and bloats every run.
5. **Test against the catalog** before adding: run one task through the new lens and its nearest built-in neighbor. If observations overlap more than ~50%, refine or merge instead of adding.
6. **Weight conservatively.** New lenses enter at weight 1 by default and earn higher default weights in profiles only after proving they change conclusions.

## Example custom lenses

```markdown
## Legal & Compliance

- **Description:** Regulatory-exposure analysis of a plan or product.
- **Goal:** Flag actions that create legal or compliance obligations before they are taken.
- **Reasoning strategy:** Enumerate jurisdictions and applicable regimes (privacy, consumer,
  sector-specific); map each planned action to the obligations it triggers; flag, never conclude —
  output is "consult counsel about X", not legal advice.
- **Fixed questions:**
  - What regulations plausibly apply here?
  - What data or actions create obligations?
  - What would a regulator object to first?
- **Expected outputs:** Flags list: action, regime, obligation triggered, severity of exposure.
- **Cost:** Medium.
- **Recommended for:** Products handling personal data, financial features, cross-border launches.
- **Do NOT use when:** Purely internal technical work with no data or market exposure.
```

```markdown
## Sustainability

- **Description:** Resource- and long-term-viability analysis.
- **Goal:** Surface hidden ongoing costs — energy, maintenance, attention — of a proposed solution.
- **Reasoning strategy:** Project the solution 2 and 10 years out; estimate recurring resource
  consumption and maintenance load; identify what silently degrades without continued investment.
- **Fixed questions:**
  - What does this consume every month it exists?
  - Who maintains this in five years?
  - What degrades if everyone stops paying attention?
- **Expected outputs:** Recurring-cost inventory and the single largest long-term liability.
- **Cost:** Low.
- **Recommended for:** Infrastructure choices, process adoption, dependency decisions.
- **Do NOT use when:** Deliberately short-lived work (prototypes, one-off scripts) — flag the
  assumption of short life instead.
```

```markdown
## Storytelling

- **Description:** Narrative-structure analysis of communication artifacts.
- **Goal:** Make the material land as a story: tension, stakes, resolution, memorability.
- **Fixed questions:**
  - What is the tension that makes someone keep reading?
  - Whose story is this, and do we stay in it?
  - What single line should the audience remember?
- **Reasoning strategy:** Locate the protagonist and the stakes; check that structure escalates
  rather than lists; compress the message to one memorable sentence and verify the artifact earns it.
- **Expected outputs:** Structural notes plus the proposed one-line takeaway.
- **Cost:** Low.
- **Recommended for:** Creative writing, talks, pitches, launch posts, documentation intros.
- **Do NOT use when:** Reference material where scanability beats narrative (API docs, runbooks).
```
