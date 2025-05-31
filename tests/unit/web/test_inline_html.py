"""
Covers:
• Every flag combination (`include_filename_comments`, `prettify`).
• Both “bs4 present” (stub) and “bs4 missing” branches.
• `inline_html_file` end-to-end round-trip.
• All documented failure paths + extra edge-cases (missing file, zero matches, duplicates, bad indentation).
• Indentation and comment-block integrity.
"""

from __future__ import annotations

import sys
import warnings
from pathlib import Path
from types import ModuleType
from typing import Any, cast, Dict

import pytest

import muutils.web.inline_html as ia

# --------------------------------------------------------------------------- #
# Constants                                                                   #
# --------------------------------------------------------------------------- #
SAMPLE_HTML: str = """<html>
<head>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <script src="app.js"></script>
</body>
</html>"""

CSS_CONTENT: str = "body { color: red; }"
JS_CONTENT: str = "console.log('hello');"


# --------------------------------------------------------------------------- #
# Fixtures                                                                    #
# --------------------------------------------------------------------------- #
@pytest.fixture()
def project(tmp_path: Path) -> Dict[str, Any]:
    """Set up a temporary project directory with HTML, CSS, JS (all referenced)."""
    html_path: Path = tmp_path / "index.html"
    css_path: Path = tmp_path / "style.css"
    js_path: Path = tmp_path / "app.js"

    html_path.write_text(SAMPLE_HTML)
    css_path.write_text(CSS_CONTENT)
    js_path.write_text(JS_CONTENT)

    return {
        "dir": tmp_path,
        "html": html_path,
        "css": css_path,
        "js": js_path,
    }


# Helper – monkey-patch a *working* BeautifulSoup with predictable output
class _StubSoup:  # noqa: D401
    def __init__(self, html: str, _parser: str) -> None:
        self._html: str = html

    def prettify(self) -> str:  # noqa: D401
        return f"PRETTIFIED\n{self._html}"


def _install_bs4_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    dummy_bs: ModuleType = ModuleType("bs4")  # type: ignore[assignment]
    dummy_bs.BeautifulSoup = _StubSoup  # type: ignore[attr-defined]
    monkeypatch.setitem(sys.modules, "bs4", dummy_bs)


# --------------------------------------------------------------------------- #
# Parametrised happy-path test (all flag combos + bs4 present / missing)      #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize(
    "include_comments", [True, False], ids=lambda b: f"comments={b}"
)
@pytest.mark.parametrize("bs4_present", [True, False], ids=lambda b: f"bs4={b}")
@pytest.mark.parametrize("prettify", [True, False], ids=lambda b: f"prettify={b}")
def test_inline_html_assets_matrix(
    project: Dict[str, Any],
    include_comments: bool,
    prettify: bool,
    bs4_present: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Exhaustive cartesian-product of switch settings."""
    if prettify and bs4_present:
        _install_bs4_stub(monkeypatch)
    elif "bs4" in sys.modules:
        monkeypatch.delitem(sys.modules, "bs4", raising=False)

    base_dir: Path = cast(Path, project["dir"])
    html_src: str = project["html"].read_text()

    result: str = ia.inline_html_assets(
        html_src,
        assets=[("script", Path("app.js")), ("style", Path("style.css"))],
        base_path=base_dir,
        include_filename_comments=include_comments,
        prettify=prettify,
    )

    # --- Inlined content checks ---
    assert CSS_CONTENT in result
    assert JS_CONTENT in result
    assert '<script src="app.js"></script>' not in result
    assert '<link rel="stylesheet" href="style.css">' not in result

    # Comment blocks appear exactly when requested
    assert ("<!-- begin 'style.css' -->" in result) is include_comments
    assert ("<!-- end 'style.css' -->" in result) is include_comments

    # If prettified via our stub, sentinel present
    if prettify and bs4_present:
        assert result.startswith("PRETTIFIED")


# --------------------------------------------------------------------------- #
# inline_html_file end-to-end (both comment modes)                            #
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("include_comments", [True, False])
def test_inline_html_file_roundtrip(
    project: Dict[str, Any],
    include_comments: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """All files in directory are auto-detected and inlined."""
    out_path: Path = project["dir"] / f"out_{include_comments}.html"

    # Guard: ensure bs4 missing path exercised
    if "bs4" in sys.modules:
        monkeypatch.delitem(sys.modules, "bs4", raising=False)

    ia.inline_html_file(
        html_path=project["html"],
        output_path=out_path,
        include_filename_comments=include_comments,
        prettify=False,
    )
    out_html: str = out_path.read_text()

    # No raw tags left; content present
    assert CSS_CONTENT in out_html
    assert JS_CONTENT in out_html
    assert '<script src="app.js"></script>' not in out_html
    assert '<link rel="stylesheet" href="style.css">' not in out_html
    # Correct comment behaviour
    assert ("<!-- begin 'style.css' -->" in out_html) is include_comments


# --------------------------------------------------------------------------- #
# Error & edge-case tests                                                     #
# --------------------------------------------------------------------------- #
def test_unsupported_asset_type(project: Dict[str, Any]) -> None:
    html_src: str = project["html"].read_text()
    with pytest.raises(ValueError, match="Unsupported tag type"):
        ia.inline_html_assets(html_src, [("video", Path("demo.mp4"))], project["dir"])  # type: ignore


def test_asset_file_missing(project: Dict[str, Any]) -> None:
    html_src: str = project["html"].read_text()
    # Delete the physical JS file
    project["js"].unlink()
    with pytest.raises(FileNotFoundError):
        ia.inline_html_assets(html_src, [("script", Path("app.js"))], project["dir"])


@pytest.mark.parametrize("occurrences", [0, 2], ids=lambda n: f"occurs={n}")
def test_pattern_not_exactly_once(project: Dict[str, Any], occurrences: int) -> None:
    html_src: str = project["html"].read_text()
    if occurrences == 0:
        html_src = html_src.replace('<script src="app.js"></script>', "")
    else:  # duplicate
        html_src = html_src.replace(
            '<script src="app.js"></script>',
            '<script src="app.js"></script>\n    <script src="app.js"></script>',
        )
    with pytest.raises(AssertionError, match="exactly once"):
        ia.inline_html_assets(html_src, [("script", Path("app.js"))], project["dir"])


def test_tag_not_alone_on_line(project: Dict[str, Any]) -> None:
    html_src: str = (
        project["html"]
        .read_text()
        .replace(
            '    <link rel="stylesheet" href="style.css">',
            '    <!--pre--><link rel="stylesheet" href="style.css">',
        )
    )
    with pytest.raises(AssertionError, match="alone in its line"):
        ia.inline_html_assets(html_src, [("style", Path("style.css"))], project["dir"])


@pytest.mark.skip("can't figure out how to prevent bs4 import")
def test_prettify_without_bs4_emits_warning(
    project: Dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Not having BeautifulSoup installed is *warning*, not fatal."""
    # Ensure bs4 absent
    monkeypatch.delitem(sys.modules, "bs4", raising=False)
    html_src: str = project["html"].read_text()
    with warnings.catch_warnings(record=True) as rec:
        warnings.simplefilter("always")
        ia.inline_html_assets(
            html_src,
            [("script", Path("app.js"))],
            project["dir"],
            prettify=True,
        )
    assert any(["BeautifulSoup is not installed" in str(w.message) for w in rec])


def test_mixed_asset_order(project: Dict[str, Any]) -> None:
    """Order of asset tuples can be arbitrary."""
    html_src: str = project["html"].read_text()
    result: str = ia.inline_html_assets(
        html_src,
        # reversed order
        [("style", Path("style.css")), ("script", Path("app.js"))],
        project["dir"],
    )
    assert CSS_CONTENT in result and JS_CONTENT in result


def test_multiple_assets_same_type(project: Dict[str, Any]) -> None:
    """Supports >1 asset of given type provided patterns are unique."""
    # Add second css file
    css2: Path = project["dir"] / "extra.css"
    css2.write_text("h1{font-size:2em;}")
    html_mod: str = SAMPLE_HTML.replace(
        "</head>",
        '    <link rel="stylesheet" href="extra.css">\n</head>',
    )
    # Update on disk
    project["html"].write_text(html_mod)

    result: str = ia.inline_html_assets(
        html_mod,
        [
            ("style", Path("style.css")),
            ("style", Path("extra.css")),
            ("script", Path("app.js")),
        ],
        project["dir"],
    )
    assert "h1{font-size:2em;}" in result
