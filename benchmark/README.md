# Micro-benchmark: direct answer vs. latent mode vs. full engine

Five tasks, each answered three ways, scored against a fixed rubric. The goal is to make the framework's cost/quality trade-off **inspectable** — every answer is in [answers/](answers/), every score in [results.json](results.json), and the charts are regenerated from the data by [render_charts.py](render_charts.py).

## Read this first: limitations

This is an **illustrative, self-evaluated micro-benchmark**, not scientific evidence.

- **N = 5 tasks.** Enough to show the shape of the trade-off, nowhere near enough for statistical claims.
- **Same model generated and judged all answers.** Self-judging is biased toward whatever the judge finds articulate. The rubric and raw answers are published precisely so you can disagree.
- **Token cost is approximated by word count** of the visible output (thinking tokens excluded). Real ratios vary by model and settings.
- **The engine's cost is under-stated here.** The `engine` answers are *condensed* transcripts (~200 words); a real explicit run generates several times more intermediate lens text than the summary shows — the full worked run of task 1 in [examples/with-vs-without.md](../examples/with-vs-without.md) is ~1,200 words. Read the engine's word counts as a floor, not the bill.
- Tasks 1–4 are deliberately good fits for the framework; task 5 is a deliberate poor fit (control). A benchmark of only good fits would be marketing.

To make this rigorous you would want: independent judge models, blinded A/B ordering, many more tasks, and human raters. The file layout supports swapping in exactly that — PRs welcome.

## The three modes

| Mode | What it is | Expected cost |
|---|---|---|
| `baseline` | Direct single-pass answer, no framework | 1× |
| `latent` | One pass, primed with the selected lenses' questions; mandatory slots for challenged premise, named risk, confidence ([latent-mode.md](../skills/cognitive-lenses/references/latent-mode.md)) | ~1–2× |
| `engine` | Full explicit pipeline: planner → lenses → consensus → self-critique | ~10–20× |

## Rubric (0–5 per dimension)

Defined in [rubric.md](rubric.md):

1. **Premise scrutiny** — did the answer test the question's own assumptions?
2. **Risk & blind-spot coverage** — material risks, second-order effects, affected people.
3. **Actionability** — concrete, correctly-sequenced next steps.
4. **Calibration** — is uncertainty stated honestly and proportionately?

## Results snapshot

See the charts in the repo README, or regenerate:

```bash
python benchmark/render_charts.py   # needs matplotlib
```

Headline pattern (read with the limitations above):

- On good-fit tasks, the **engine** scores highest, driven by premise scrutiny and risk coverage.
- **Latent mode** captures most of the engine's quality gain at a fraction of the cost — it is the trade-off sweet spot for everyday questions.
- On the poor-fit control task, **baseline wins**: the engine pays ~100× the words for a slightly *worse* answer (the value is buried). The Planner's go/no-go duty is not decorative.
