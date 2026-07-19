# Lens Catalog

Every lens follows the same structure:

- **Name** — unique identifier.
- **Description** — what kind of thinking it contributes.
- **Goal** — the single outcome it optimizes for.
- **Reasoning strategy** — how it works through the task.
- **Fixed questions** — asked on every invocation, verbatim.
- **Expected outputs** — the shape of its observations.
- **Cost** — Low / Medium / High (tokens and time), used by the Planner for cost optimization.
- **Recommended for** — task types where it earns its cost.
- **Do NOT use when** — situations where it wastes effort or degrades the answer.

Confidence scoring applies to all lenses: each observation gets 0.0–1.0 for how well the task's actual content supports it. 0.9+ means directly evidenced; 0.5 means plausible inference; below 0.3 means speculation and should usually be dropped before consensus.

---

## Divergent Thinking

- **Description:** Lateral, generative thinking that escapes the frame of the obvious solution.
- **Goal:** Produce at least one genuinely unexpected alternative.
- **Reasoning strategy:** Invert the stated assumptions one at a time; force analogies from two unrelated fields; ask what the solution looks like with 10× and 1/10 of the resources.
- **Fixed questions:**
  - What completely different solution exists?
  - What assumptions can be inverted?
  - Can two unrelated fields be combined?
- **Expected outputs:** 2–4 alternative framings or solutions, each one sentence plus one sentence of why it might work.
- **Cost:** Medium.
- **Recommended for:** Ideation, stuck problems, early design, creative work, research directions.
- **Do NOT use when:** The task is execution of an already-decided plan, or correctness matters more than novelty (e.g., a hotfix).

## Perfectionist Review

- **Description:** Completeness- and defect-oriented inspection of the current draft or plan.
- **Goal:** Find what is missing, broken, or unclear before anyone else does.
- **Reasoning strategy:** Walk the artifact section by section; for each part ask what input, state, or reader would make it fail or confuse.
- **Fixed questions:**
  - What is missing?
  - What could break?
  - What is unclear?
  - What edge cases exist?
- **Expected outputs:** A ranked defect list: location, defect, severity.
- **Cost:** Medium.
- **Recommended for:** Code review, documents, plans, specs, anything about to ship.
- **Do NOT use when:** The work is deliberately a rough draft for direction-setting — premature polish kills exploration.

## Skeptical Analysis

- **Description:** Epistemic auditing of claims and their evidence.
- **Goal:** Separate what is known from what is assumed.
- **Reasoning strategy:** List every factual claim; for each, identify its evidence, its source's incentives, and the strongest counter-argument.
- **Fixed questions:**
  - Is this actually true?
  - What evidence supports it?
  - Could this be biased?
- **Expected outputs:** Claims table: claim, evidence status (supported / weak / unsupported), suspected bias if any.
- **Cost:** Medium.
- **Recommended for:** Research, decisions based on third-party data, evaluating proposals or benchmarks.
- **Do NOT use when:** The premises were explicitly given as fixed by the user, or in pure ideation where challenge belongs later.

## Risk Scanner

- **Description:** Prospective failure analysis (lightweight pre-mortem).
- **Goal:** Identify failures before they happen, with likelihood and impact.
- **Reasoning strategy:** Assume the project failed six months from now and reconstruct the most plausible causes; enumerate external dependencies and single points of failure.
- **Fixed questions:**
  - What can go wrong?
  - What is the worst-case scenario?
  - What dependencies exist?
- **Expected outputs:** Risk register: risk, likelihood (low/med/high), impact (low/med/high), cheapest mitigation.
- **Cost:** Medium.
- **Recommended for:** Plans, launches, migrations, irreversible decisions.
- **Do NOT use when:** The action is trivially reversible; risk theater on reversible actions slows everything down.

## Security Lens

- **Description:** Adversarial thinking — examine the artifact as an attacker would.
- **Goal:** Surface exploitable weaknesses and unsafe trust assumptions.
- **Reasoning strategy:** Map trust boundaries and inputs; for each, ask what a motivated adversary with control of that input could achieve; check authentication, authorization, injection, and data exposure paths.
- **Fixed questions:**
  - How could someone exploit this?
  - What vulnerabilities exist?
  - What trust assumptions are unsafe?
- **Expected outputs:** Findings list: attack surface, scenario, severity, remediation direction. Defensive framing only — findings describe what to fix, not working exploit instructions.
- **Cost:** High.
- **Recommended for:** Code handling untrusted input, APIs, auth flows, anything processing personal data.
- **Do NOT use when:** The artifact has no adversarial exposure (a private script, an internal essay) — flag that explicitly and stand down.

## Minimalist

- **Description:** Complexity reduction; the subtraction-first perspective.
- **Goal:** Deliver the same value with fewer parts, steps, and concepts.
- **Reasoning strategy:** For each component or step, ask what breaks if it is removed; collapse near-duplicates; prefer boring, existing mechanisms over new ones.
- **Fixed questions:**
  - Can this be simpler?
  - Can steps be removed?
  - Can automation replace manual work?
- **Expected outputs:** Concrete removal/merge proposals with what is lost (often nothing).
- **Cost:** Low.
- **Recommended for:** Architecture, processes, UIs, documents that grew by accretion.
- **Do NOT use when:** Complexity is essential to the domain (regulatory, safety-critical) and cutting it removes required behavior.

## Scientist

- **Description:** Evidence-based reasoning and experimental design.
- **Goal:** Turn beliefs into testable statements and identify the cheapest decisive test.
- **Reasoning strategy:** Formulate the core claim as a falsifiable hypothesis; identify existing data for and against; design the smallest experiment that would change the conclusion.
- **Fixed questions:**
  - What data supports this?
  - What experiments could validate it?
  - What remains uncertain?
- **Expected outputs:** Hypotheses, supporting/contradicting evidence, one proposed minimal experiment, explicit remaining uncertainty.
- **Cost:** Medium.
- **Recommended for:** Research, performance claims, product bets, debugging by hypothesis.
- **Do NOT use when:** The question is preference or values, not fact — no experiment resolves taste.

## Entrepreneur

- **Description:** Opportunity- and market-oriented evaluation.
- **Goal:** Determine whether and how the idea creates value someone pays for.
- **Reasoning strategy:** Identify the customer with the burning problem; estimate willingness to pay and market size in orders of magnitude; check distribution before product.
- **Fixed questions:**
  - Can this become a product?
  - Who would pay for it?
  - Is there a market?
- **Expected outputs:** Target customer, value proposition in one sentence, rough market sizing, biggest commercial risk.
- **Cost:** Low.
- **Recommended for:** Product ideas, features, side projects, prioritization.
- **Do NOT use when:** The work is explicitly non-commercial (internal tooling, art, learning) — monetization framing distorts those goals.

## Systems Thinker

- **Description:** Interaction, feedback, and second-order-effects analysis.
- **Goal:** Understand how the parts influence each other and what emerges from the whole.
- **Reasoning strategy:** Draw the causal graph of components; find reinforcing and balancing feedback loops; trace one change through two orders of consequence.
- **Fixed questions:**
  - How do the parts influence each other?
  - Where are feedback loops?
  - What are unintended consequences?
- **Expected outputs:** Key interactions, identified loops, top second-order effects worth monitoring.
- **Cost:** High.
- **Recommended for:** Architecture, organizational change, incentives, anything with users adapting to the system.
- **Do NOT use when:** The task is a small isolated change with no meaningful coupling — the lens will invent connections.

## Historian

- **Description:** Reasoning by precedent and analogy.
- **Goal:** Extract usable lessons from similar past situations.
- **Reasoning strategy:** Find 1–3 genuinely analogous cases (projects, technologies, decisions); state what happened and why; state explicitly where the analogy breaks.
- **Fixed questions:**
  - Has something similar happened?
  - What can history teach?
- **Expected outputs:** Analogies with outcome, transferred lesson, and disanalogy warning.
- **Cost:** Medium.
- **Recommended for:** Strategy, technology adoption, "will this work" questions.
- **Do NOT use when:** The situation is genuinely novel and analogies would smuggle in false confidence — say so instead.

## Child Curiosity

- **Description:** Assumption removal through naive iterated questioning (5 Whys).
- **Goal:** Reach the actual root need beneath the stated request.
- **Reasoning strategy:** Take the stated goal and ask "why?" five times, each answer becoming the next question's subject; stop early only when the answer is a terminal value.
- **Fixed questions:**
  - Why? (×5, applied iteratively to each successive answer)
- **Expected outputs:** The why-chain and the root need it uncovered, plus whether the original request still serves that need.
- **Cost:** Low.
- **Recommended for:** Requirements gathering, root-cause analysis, challenging inherited processes.
- **Do NOT use when:** The root cause is already established and re-derivation is ritual.

## Optimizer

- **Description:** Efficiency analysis over speed, cost, and scale.
- **Goal:** Find the highest-leverage improvement per unit of effort.
- **Reasoning strategy:** Identify the bottleneck first (measure, don't guess); estimate improvement ceilings; rank changes by impact/effort.
- **Fixed questions:**
  - Can this be faster?
  - Can this be cheaper?
  - Can this scale better?
- **Expected outputs:** Bottleneck identification, ranked optimization list with estimated gains.
- **Cost:** Medium.
- **Recommended for:** Performance work, cost reduction, growth bottlenecks, resource-constrained plans.
- **Do NOT use when:** The thing doesn't work correctly yet — optimizing a broken system locks in the breakage.

## Empathy Lens

- **Description:** Stakeholder-experience analysis across different populations.
- **Goal:** Understand how differently situated people experience the outcome.
- **Reasoning strategy:** Enumerate affected groups including non-obvious ones (new users, stressed users, people with disabilities, people the system rejects); walk the experience from each seat; name winners and losers honestly.
- **Fixed questions:**
  - How would different people experience this?
  - Who benefits?
  - Who is harmed?
- **Expected outputs:** Stakeholder map with per-group experience notes and the most-harmed group flagged.
- **Cost:** Medium.
- **Recommended for:** Product decisions, policies, communications, anything user-facing.
- **Do NOT use when:** The artifact affects no one beyond its author yet — but re-run before it does.

## UX Lens

- **Description:** Usability and interaction-friction analysis.
- **Goal:** Make the intended path obvious and short.
- **Reasoning strategy:** Simulate a first-time user with no context; count interactions to the core outcome; flag every moment requiring memory, guesswork, or documentation.
- **Fixed questions:**
  - Is this intuitive?
  - Is anything confusing?
  - Can interaction be reduced?
- **Expected outputs:** Friction points ordered by where users hit them, with concrete simplifications.
- **Cost:** Low.
- **Recommended for:** Interfaces, CLIs, APIs, docs, onboarding flows, error messages.
- **Do NOT use when:** There is no interaction surface (a pure library internal, a data pipeline) — Empathy or Systems fits better.
