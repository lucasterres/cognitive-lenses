"""Render the benchmark comparison charts (light and dark variants).

Reads scores from results.json and computes cost (visible words) directly from
the answer files, then writes four PNGs into docs/img/.

Usage:  python benchmark/render_charts.py
Needs:  matplotlib
"""

import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
import matplotlib.patches as mpatches

ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "docs" / "img"

MODES = ["baseline", "latent", "engine"]
MODE_LABELS = {"baseline": "Baseline", "latent": "Latent mode", "engine": "Full engine"}

# Validated 3-slot categorical palette (dataviz reference palette, slots 1-3).
THEMES = {
    "light": {
        "series": {"baseline": "#2a78d6", "latent": "#008300", "engine": "#e87ba4"},
        "surface": "#fcfcfb", "ink": "#0b0b0b", "ink2": "#52514e",
        "muted": "#898781", "grid": "#e1e0d9", "baseline_ax": "#c3c2b7",
    },
    "dark": {
        "series": {"baseline": "#3987e5", "latent": "#008300", "engine": "#d55181"},
        "surface": "#1a1a19", "ink": "#ffffff", "ink2": "#c3c2b7",
        "muted": "#898781", "grid": "#2c2c2a", "baseline_ax": "#383835",
    },
}

plt.rcParams.update({
    "font.family": ["Segoe UI", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
})


def load_data():
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    tasks = results["tasks"]
    for task in tasks:
        text = (ROOT / "answers" / f"{task['id']}.md").read_text(encoding="utf-8")
        task["words"] = {}
        for mode in MODES:
            match = re.search(rf"^## {mode}\n(.*?)(?=^## |\Z)", text,
                              flags=re.MULTILINE | re.DOTALL)
            task["words"][mode] = len(match.group(1).split())
        task["mean"] = {
            mode: sum(task["scores"][mode].values()) / len(task["scores"][mode])
            for mode in MODES
        }
    return tasks


def rounded_top_bar(ax, x, width, height, color, px_radius=4):
    """Bar with only its data-end (top) rounded, anchored flat to the baseline."""
    fig = ax.figure
    fig.canvas.draw()
    (x0, y0), (x1, y1) = ax.transData.transform([(0, 0), (1, 1)])
    rx = min(px_radius / abs(x1 - x0), width / 2)
    ry = min(px_radius / abs(y1 - y0), height)
    left, right, top = x, x + width, height
    verts = [
        (left, 0), (left, top - ry), (left, top), (left + rx, top),
        (right - rx, top), (right, top), (right, top - ry), (right, 0), (left, 0),
    ]
    codes = [
        MplPath.MOVETO, MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3,
        MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO,
        MplPath.CLOSEPOLY,
    ]
    ax.add_patch(mpatches.PathPatch(MplPath(verts, codes), facecolor=color,
                                    edgecolor="none", zorder=3))


def style_axes(ax, theme):
    ax.set_facecolor(theme["surface"])
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color(theme["baseline_ax"])
    ax.tick_params(colors=theme["muted"], labelsize=9, length=0)
    ax.yaxis.grid(True, color=theme["grid"], linewidth=0.8, zorder=0)
    ax.xaxis.grid(False)
    ax.set_axisbelow(True)


def titles(fig, title, subtitle, theme):
    fig.text(0.06, 0.955, title, fontsize=14, fontweight="bold", color=theme["ink"])
    fig.text(0.06, 0.905, subtitle, fontsize=9.5, color=theme["ink2"])


def legend(owner, theme, handles, labels, **kwargs):
    leg = owner.legend(handles, labels, frameon=False, fontsize=9,
                       handlelength=1.1, handleheight=1.1, **kwargs)
    for text in leg.get_texts():
        text.set_color(theme["ink2"])
    return leg


def chart_scores(tasks, mode_name, theme):
    fig, ax = plt.subplots(figsize=(8.6, 4.4), dpi=150)
    fig.patch.set_facecolor(theme["surface"])
    ax.set_xlim(0.4, len(tasks) + 0.6)
    ax.set_ylim(0, 5.35)

    group_width, n = 0.62, len(MODES)
    fig.canvas.draw()
    (px0, _), (px1, _) = ax.transData.transform([(0, 0), (1, 0)])
    gap = 2 / abs(px1 - px0)  # 2px surface gap between adjacent bars
    bar_w = (group_width - gap * (n - 1)) / n

    for gi, task in enumerate(tasks, start=1):
        for mi, mode in enumerate(MODES):
            bx = gi - group_width / 2 + mi * (bar_w + gap)
            value = task["mean"][mode]
            rounded_top_bar(ax, bx, bar_w, value, theme["series"][mode])
            ax.text(bx + bar_w / 2, value + 0.12, f"{value:.1f}",
                    ha="center", va="bottom", fontsize=7.5, color=theme["ink2"])

    ax.set_xticks(range(1, len(tasks) + 1))
    labels = [task["title"].replace(" (control)", "\n(control · poor fit)")
              for task in tasks]
    ax.set_xticklabels(labels, fontsize=8.4, color=theme["ink2"])
    ax.set_yticks(range(6))
    ax.set_ylabel("Mean rubric score (0–5)", fontsize=9, color=theme["muted"])
    style_axes(ax, theme)

    handles = [mpatches.Patch(facecolor=theme["series"][m], edgecolor="none")
               for m in MODES]
    legend(fig, theme, handles, [MODE_LABELS[m] for m in MODES],
           ncol=3, loc="upper right", bbox_to_anchor=(0.97, 0.895),
           columnspacing=1.2)
    titles(fig, "Answer quality: with vs. without the engine",
           "Mean score across premise scrutiny, risk coverage, actionability, calibration"
           " · self-judged illustrative micro-benchmark (N=5)", theme)
    fig.subplots_adjust(left=0.075, right=0.97, top=0.80, bottom=0.15)
    fig.savefig(OUT / f"benchmark-scores-{mode_name}.png",
                facecolor=theme["surface"])
    plt.close(fig)


def chart_tradeoff(tasks, mode_name, theme):
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
    fig.patch.set_facecolor(theme["surface"])
    markers = {"baseline": "o", "latent": "s", "engine": "^"}

    for mode in MODES:
        xs = [task["words"][mode] for task in tasks]
        ys = [task["mean"][mode] for task in tasks]
        ax.scatter(xs, ys, s=70, marker=markers[mode],
                   facecolor=theme["series"][mode], edgecolor=theme["surface"],
                   linewidth=2, zorder=3, label=MODE_LABELS[mode])

    control = next(task for task in tasks if task["framework_fit"] == "poor")
    for mode in ("baseline", "engine"):
        x, y = control["words"][mode], control["mean"][mode]
        note = ("control task: the engine\npays 79 words to score lower"
                if mode == "engine" else "control task:\n1 word, perfect answer")
        offset = (10, -30) if mode == "engine" else (8, 8)
        ax.annotate(note, (x, y), textcoords="offset points", xytext=offset,
                    fontsize=7.8, color=theme["muted"], style="italic")

    # direct cluster labels (identity never rides on color alone)
    good = [task for task in tasks if task["framework_fit"] == "good"]
    cluster_offsets = {"baseline": (0, -0.38), "latent": (0, -0.38),
                       "engine": (0, 0.22)}
    for mode in MODES:
        cx = sum(task["words"][mode] for task in good) / len(good)
        cy = sum(task["mean"][mode] for task in good) / len(good)
        dx, dy = cluster_offsets[mode]
        ax.text(cx + dx, cy + dy, MODE_LABELS[mode], ha="center",
                fontsize=8.6, color=theme["ink2"], fontweight="bold")

    ax.set_xscale("log")
    ax.set_xticks([1, 10, 30, 100, 300])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.set_xlabel("Visible words per answer (log scale — cost proxy)",
                  fontsize=9, color=theme["muted"])
    ax.set_ylabel("Mean rubric score (0–5)", fontsize=9, color=theme["muted"])
    ax.set_ylim(1.85, 5.3)
    ax.set_yticks([2, 3, 4, 5])
    style_axes(ax, theme)

    handles, labels = ax.get_legend_handles_labels()
    legend(ax, theme, handles, labels, loc="lower left", borderaxespad=0.6)
    titles(fig, "Quality vs. token cost, per task and mode",
           "Latent mode captures most of the quality gain at a fraction of the cost"
           " · same data as the bars", theme)
    fig.subplots_adjust(left=0.075, right=0.97, top=0.84, bottom=0.14)
    fig.savefig(OUT / f"benchmark-tradeoff-{mode_name}.png",
                facecolor=theme["surface"])
    plt.close(fig)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tasks = load_data()
    for mode_name, theme in THEMES.items():
        chart_scores(tasks, mode_name, theme)
        chart_tradeoff(tasks, mode_name, theme)
    for task in tasks:
        means = "  ".join(f"{m}={task['mean'][m]:.1f}/{task['words'][m]}w"
                          for m in MODES)
        print(f"{task['id']}: {means}")
    print(f"charts written to {OUT}")


if __name__ == "__main__":
    main()
