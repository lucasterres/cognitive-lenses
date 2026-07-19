"""Structural tests for the cognitive-lenses skill.

Run with ``pytest`` or plain ``python tests/test_skill_structure.py`` — no
dependencies beyond the standard library.

These tests enforce the framework's own contracts:
- the skill manifest (SKILL.md) is well-formed and every referenced file exists;
- the catalog contains the full lens set, each with every required field;
- the adaptive-selection profiles only reference lenses that actually exist;
- community lens examples follow the mandatory template.
"""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_DIR = REPO_ROOT / "skills" / "cognitive-lenses"
REFERENCES = SKILL_DIR / "references"

EXPECTED_LENSES = [
    "Divergent Thinking",
    "Perfectionist Review",
    "Skeptical Analysis",
    "Risk Scanner",
    "Security Lens",
    "Minimalist",
    "Scientist",
    "Entrepreneur",
    "Systems Thinker",
    "Historian",
    "Child Curiosity",
    "Optimizer",
    "Empathy Lens",
    "UX Lens",
]

REQUIRED_FIELDS = [
    "Description",
    "Goal",
    "Reasoning strategy",
    "Fixed questions",
    "Expected outputs",
    "Cost",
    "Recommended for",
    "Do NOT use when",
]

VALID_COSTS = {"Low", "Medium", "High"}


def read(path: Path) -> str:
    assert path.is_file(), f"missing file: {path.relative_to(REPO_ROOT)}"
    return path.read_text(encoding="utf-8")


def lens_sections(catalog_text: str) -> dict:
    """Map lens name -> section body, from '## Name' headings."""
    sections = {}
    parts = re.split(r"^## ", catalog_text, flags=re.MULTILINE)[1:]
    for part in parts:
        name, _, body = part.partition("\n")
        sections[name.strip()] = body
    return sections


# --- SKILL.md manifest -------------------------------------------------------

def test_skill_md_frontmatter():
    text = read(SKILL_DIR / "SKILL.md")
    match = re.match(r"^---\n(.*?)\n---\n", text, flags=re.DOTALL)
    assert match, "SKILL.md must start with YAML frontmatter"
    front = match.group(1)
    name = re.search(r"^name:\s*(\S+)\s*$", front, flags=re.MULTILINE)
    assert name and name.group(1) == "cognitive-lenses", "frontmatter name must be 'cognitive-lenses'"
    desc = re.search(r"^description:\s*(.+)$", front, flags=re.MULTILINE)
    assert desc and len(desc.group(1).strip()) >= 100, "description must exist and be substantive"
    assert len(desc.group(1)) <= 1024, "description must stay within 1024 characters"


def test_skill_md_covers_pipeline_stages():
    text = read(SKILL_DIR / "SKILL.md")
    for stage in ["Planner", "Consensus Engine", "Self Critique", "Final Answer"]:
        assert stage in text, f"SKILL.md must describe the '{stage}' stage"


def test_all_markdown_links_resolve():
    for md in [SKILL_DIR / "SKILL.md", *REFERENCES.glob("*.md")]:
        text = read(md)
        for label, target in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            resolved = (md.parent / target.split("#")[0]).resolve()
            assert resolved.is_file(), (
                f"{md.name}: link '{label}' -> '{target}' does not resolve"
            )


# --- Lens catalog ------------------------------------------------------------

def test_catalog_contains_all_expected_lenses():
    sections = lens_sections(read(REFERENCES / "lens-catalog.md"))
    for lens in EXPECTED_LENSES:
        assert lens in sections, f"catalog is missing lens '{lens}'"


def test_every_lens_has_all_required_fields():
    sections = lens_sections(read(REFERENCES / "lens-catalog.md"))
    for lens in EXPECTED_LENSES:
        body = sections[lens]
        for field in REQUIRED_FIELDS:
            assert f"**{field}:**" in body, f"lens '{lens}' is missing field '{field}'"


def test_lens_costs_are_valid():
    sections = lens_sections(read(REFERENCES / "lens-catalog.md"))
    for lens in EXPECTED_LENSES:
        match = re.search(r"\*\*Cost:\*\*\s*(\w+)", sections[lens])
        assert match, f"lens '{lens}' has no parsable Cost"
        assert match.group(1) in VALID_COSTS, (
            f"lens '{lens}' cost '{match.group(1)}' not in {sorted(VALID_COSTS)}"
        )


def test_every_lens_has_fixed_questions():
    sections = lens_sections(read(REFERENCES / "lens-catalog.md"))
    for lens in EXPECTED_LENSES:
        body = sections[lens]
        questions_block = body.split("**Fixed questions:**", 1)[1]
        questions_block = questions_block.split("**Expected outputs:**", 1)[0]
        bullets = re.findall(r"^\s+- .+$", questions_block, flags=re.MULTILINE)
        assert bullets, f"lens '{lens}' declares no fixed questions"


# --- Adaptive selection ------------------------------------------------------

def canonical_lens(name: str) -> str:
    """Normalize a profile-table mention to a catalog heading, or return '' if unknown."""
    name = re.sub(r"\s*\([^)]*\)", "", name).strip()
    if not name or name == "—":
        return ""
    for candidate in (name, f"{name} Lens"):
        if candidate in EXPECTED_LENSES:
            return candidate
    return name  # unknown — caller decides


def test_selection_profiles_reference_existing_lenses():
    text = read(REFERENCES / "lens-selection.md")
    rows = [
        line for line in text.splitlines()
        if line.startswith("|") and "---" not in line and "Task type" not in line
    ]
    assert rows, "lens-selection.md must contain the profile table"
    known = set(EXPECTED_LENSES)
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        task_type = cells[0]
        for cell in cells[1:]:
            for mention in cell.split(","):
                canonical = canonical_lens(mention)
                if canonical:
                    assert canonical in known, (
                        f"profile '{task_type}' references unknown lens '{mention.strip()}'"
                    )


# --- Custom-lens template ----------------------------------------------------

def test_custom_lens_examples_follow_template():
    text = read(REFERENCES / "custom-lenses.md")
    example_blocks = re.findall(r"```markdown\n(## .+?)```", text, flags=re.DOTALL)
    # first fenced block is the empty template itself; the rest are worked examples
    examples = [b for b in example_blocks if "<Lens Name>" not in b]
    assert examples, "custom-lenses.md must ship at least one worked example"
    for block in examples:
        name = block.splitlines()[0].removeprefix("## ").strip()
        for field in REQUIRED_FIELDS:
            assert f"**{field}:**" in block, (
                f"custom lens example '{name}' is missing field '{field}'"
            )


# --- plain-python runner -----------------------------------------------------

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
