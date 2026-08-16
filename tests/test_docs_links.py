"""Guards against broken relative links in the repo's markdown documents.

The root README, docs index, week guides, day files, and results index form
the public navigation surface of this repository. A copied-without-adjustment
edit once broke 68 links at once; this test scans every tracked markdown file
and fails on any relative link target that does not exist on disk.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
LINK_PATTERN = re.compile(r"\]\(([^)#\s]+?)(?:#[^)]*)?\)")


def _markdown_files() -> list[Path]:
    files = [p for p in REPO_ROOT.rglob("*.md") if "pdfs" not in p.parts]
    assert files, "expected markdown documents to exist"
    return files


@pytest.mark.parametrize("doc", _markdown_files(), ids=lambda p: str(p.relative_to(REPO_ROOT)))
def test_relative_links_resolve(doc: Path) -> None:
    text = doc.read_text(encoding="utf-8")
    base = doc.parent
    for link in LINK_PATTERN.findall(text):
        if link.startswith(("http://", "https://", "mailto:")):
            continue
        target = (base / link).resolve()
        assert target.exists(), f"{doc.relative_to(REPO_ROOT)} links to missing target: {link}"
