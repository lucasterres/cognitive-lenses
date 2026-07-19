"""Structural tests for the benchmark: scores, answers, and files stay in sync.

Run with ``pytest`` or plain ``python tests/test_benchmark.py``.
"""

import json
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCH = REPO_ROOT / "benchmark"

MODES = ["baseline", "latent", "engine"]


def load_results():
    return json.loads((BENCH / "results.json").read_text(encoding="utf-8"))


def test_results_json_is_well_formed():
    results = load_results()
    dims = results["rubric_dimensions"]
    assert len(dims) == 4, "rubric must have exactly 4 dimensions"
    assert results["tasks"], "benchmark must contain tasks"
    for task in results["tasks"]:
        assert task["framework_fit"] in {"good", "poor"}
        for mode in MODES:
            scores = task["scores"][mode]
            assert set(scores) == set(dims), (
                f"{task['id']}/{mode}: score dimensions must match the rubric"
            )
            for dim, value in scores.items():
                assert 0 <= value <= 5, f"{task['id']}/{mode}/{dim}: score out of range"


def test_every_task_has_an_answer_file_with_all_modes():
    results = load_results()
    for task in results["tasks"]:
        path = BENCH / "answers" / f"{task['id']}.md"
        assert path.is_file(), f"missing answer file for task '{task['id']}'"
        text = path.read_text(encoding="utf-8")
        for mode in MODES:
            match = re.search(rf"^## {mode}\n(.*?)(?=^## |\Z)", text,
                              flags=re.MULTILINE | re.DOTALL)
            assert match and match.group(1).strip(), (
                f"{task['id']}: missing or empty '## {mode}' section"
            )


def test_benchmark_includes_a_poor_fit_control():
    results = load_results()
    fits = {task["framework_fit"] for task in results["tasks"]}
    assert "poor" in fits, (
        "benchmark must keep at least one poor-fit control task — "
        "a benchmark of only good fits is marketing"
    )


def test_chart_images_exist():
    img = REPO_ROOT / "docs" / "img"
    for name in ["benchmark-scores-light.png", "benchmark-scores-dark.png",
                 "benchmark-tradeoff-light.png", "benchmark-tradeoff-dark.png",
                 "example-with-without.svg"]:
        assert (img / name).is_file(), f"missing image referenced by README: {name}"


if __name__ == "__main__":
    failures = 0
    tests = [obj for name, obj in sorted(globals().items())
             if name.startswith("test_") and callable(obj)]
    for test in tests:
        try:
            test()
            print(f"PASS  {test.__name__}")
        except AssertionError as exc:
            failures += 1
            print(f"FAIL  {test.__name__}: {exc}")
    print(f"\n{len(tests) - failures}/{len(tests)} tests passed")
    sys.exit(1 if failures else 0)
