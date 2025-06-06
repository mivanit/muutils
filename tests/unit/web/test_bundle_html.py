from __future__ import annotations

import io
import subprocess
import sys
import textwrap
import urllib.request
from pathlib import Path

import pytest

import muutils.web.bundle_html as bundle_html

# ----------------------------------------------------------------
# helper / fixtures
# ----------------------------------------------------------------


@pytest.fixture()
def site(tmp_path: Path) -> dict[str, Path]:
    """Return paths for a tiny site with four asset types."""
    css = tmp_path / "style.css"
    css.write_text("body { color: red; }")

    js = tmp_path / "app.js"
    js.write_text("console.log('hi');")

    svg = tmp_path / "icon.svg"
    svg.write_text("<svg><rect/></svg>")

    png = tmp_path / "pic.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")

    html = tmp_path / "index.html"
    html.write_text(
        textwrap.dedent(
            """\
            <!doctype html>
            <html>
              <head>
                <link   rel="stylesheet" href="style.css"   >
                <script src='app.js'></script>
              </head>
              <body>
                <img src="pic.png">
                <svg>
                  <use
                      xlink:href = "icon.svg#i" />
                </svg>
              </body>
            </html>
            """
        )
    )

    return {
        "root": tmp_path,
        "html": html,
        "css": css,
        "js": js,
        "svg": svg,
        "png": png,
    }


def _get(cfg_patch: dict | None = None) -> bundle_html.InlineConfig:
    """Return a config object with optional overrides."""
    return bundle_html.InlineConfig(**(cfg_patch or {}))


def _inline(
    text: str,
    base: Path,
    cfg_patch: dict | None = None,
) -> str:
    """Run the bundle_html with local/remote switches."""
    cfg = _get(cfg_patch)
    return bundle_html.inline_html_assets(text, base_path=base, config=cfg)


def _has_b64_fragment(html: str, mime: str) -> bool:
    """Return True if a data URI for *mime* is present."""
    return f"data:{mime};base64," in html


# ----------------------------------------------------------------
# core behaviour (regex mode)
# ----------------------------------------------------------------


def test_all_assets_inlined_regex(site: dict[str, Path]) -> None:
    html_raw = site["html"].read_text()
    out = _inline(html_raw, site["root"])
    print(out)

    assert "<style>" in out and "</style>" in out
    assert "<script>" in out and "</script>" in out
    assert _has_b64_fragment(out, "image/png")
    assert _has_b64_fragment(out, "image/svg+xml")
    assert "<!-- begin 'style.css' -->" in out
    assert "<!-- end 'app.js' -->" in out


def test_indentation_preserved(site: dict[str, Path]) -> None:
    html_raw = site["html"].read_text()
    out = _inline(html_raw, site["root"])
    # original line had 4 spaces indent
    assert "\n    <style>" in out or "\n    <script>" in out


def test_skip_large_file(site: dict[str, Path]) -> None:
    big = site["root"] / "large.js"
    big.write_bytes(b"x" * 200_000)
    site["html"].write_text(
        site["html"]
        .read_text()
        .replace("</body>", '<script src="large.js"></script>\n</body>')
    )
    out = _inline(site["html"].read_text(), site["root"], cfg_patch={"max_bytes": 1024})
    assert '<script src="large.js"></script>' in out


def test_allowed_extensions_filter(site: dict[str, Path]) -> None:
    out = _inline(
        site["html"].read_text(),
        site["root"],
        cfg_patch={"allowed_extensions": {".css"}},
    )
    assert "<style>" in out and "<script src='app.js'>" in out
    assert not _has_b64_fragment(out, "image/png")


def test_comment_toggle(site: dict[str, Path]) -> None:
    out = _inline(
        site["html"].read_text(),
        site["root"],
        cfg_patch={"include_filename_comments": False},
    )
    assert "begin 'style.css'" not in out


def test_local_off_remote_off(site: dict[str, Path]) -> None:
    out = _inline(
        site["html"].read_text(),
        site["root"],
        cfg_patch={"local": False, "remote": False},
    )
    # nothing should change
    assert '<link   rel="stylesheet" href="style.css"   >' in out


# ----------------------------------------------------------------
# remote asset handling
# ----------------------------------------------------------------


def test_remote_fetch_allowed(
    monkeypatch: pytest.MonkeyPatch, site: dict[str, Path]
) -> None:
    remote_css = "https://cdn/foo.css"
    site["html"].write_text(site["html"].read_text().replace("style.css", remote_css))

    class FakeResp(io.BytesIO):
        def __enter__(self):  # type: ignore[override]
            return self

        def __exit__(self, *exc):  # type: ignore[override]
            pass

    def fake_open(url: str, *a, **k):  # type: ignore[override]
        assert url == remote_css
        return FakeResp(b"body{background:blue;}")

    monkeypatch.setattr(urllib.request, "urlopen", fake_open)
    out = _inline(site["html"].read_text(), site["root"], cfg_patch={"remote": True})
    assert "<style>" in out and "background:blue" in out


def test_remote_disallowed(
    monkeypatch: pytest.MonkeyPatch, site: dict[str, Path]
) -> None:
    remote_css = "https://cdn/foo.css"
    site["html"].write_text(site["html"].read_text().replace("style.css", remote_css))
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: io.BytesIO(b""))
    out = _inline(site["html"].read_text(), site["root"])  # default remote=False
    assert f'href="{remote_css}"' in out  # untouched link remains


# ----------------------------------------------------------------
# bs4 mode parity checks
# ----------------------------------------------------------------


def test_bs4_matches_regex(site: dict[str, Path]) -> None:
    raw = site["html"].read_text()
    out_regex = _inline(raw, site["root"])
    out_bs4 = _inline(raw, site["root"], {"use_bs4": True})
    assert "<style>" in out_bs4 and "<style>" in out_regex
    assert _has_b64_fragment(out_bs4, "image/png")
    assert "<!-- begin 'style.css' -->" in out_bs4


def test_prettify_flag_bs4(site: dict[str, Path]) -> None:
    raw = site["html"].read_text()
    cfg = _get({"use_bs4": True})
    pretty = bundle_html.inline_html_assets(
        raw, base_path=site["root"], config=cfg, prettify=True
    )
    # prettified soup always starts with <!DOCTYPE or <html ...> on its own line
    assert pretty.lstrip().lower().startswith("<!doctype")


# ----------------------------------------------------------------
# tag_attr override
# ----------------------------------------------------------------


def test_tag_attr_override(site: dict[str, Path]) -> None:
    site["html"].write_text(site["html"].read_text().replace("href", "data-href"))
    cfg = _get({"tag_attr": {"link": "data-href"}})
    out = bundle_html.inline_html_assets(
        site["html"].read_text(), base_path=site["root"], config=cfg
    )
    assert "<style>" in out


# ----------------------------------------------------------------
# CLI integration (subprocess)
# ----------------------------------------------------------------


def test_cli_smoke(tmp_path: Path, site: dict[str, Path]) -> None:
    html_copy = tmp_path / "page.html"
    html_copy.write_text(site["html"].read_text())
    exe = Path(bundle_html.__file__).resolve()
    subprocess.check_call(
        [sys.executable, str(exe), str(html_copy), "--output", str(html_copy)]
    )

    text = html_copy.read_text()
    assert "<style>" in text and "data:image/png;base64," in text


@pytest.fixture()
def tiny_site(tmp_path: Path) -> dict[str, Path]:
    """Create a minimal web-site with one asset of each supported type."""
    css = tmp_path / "style.css"
    css.write_text("body { color: red; }")

    js = tmp_path / "app.js"
    js.write_text("console.log('hi');")

    svg = tmp_path / "icon.svg"
    svg.write_text("<svg><rect/></svg>")

    png = tmp_path / "pic.png"
    png.write_bytes(b"\x89PNG\r\n\x1a\n")  # PNG header only

    html = tmp_path / "index.html"
    html.write_text(
        textwrap.dedent(
            """
            <!doctype html>
            <html>
              <head>
                <link rel="stylesheet" href="style.css">
                <script src="app.js"></script>
              </head>
              <body>
                <img src="pic.png">
                <svg>
                  <use xlink:href="icon.svg#i"></use>
                </svg>
              </body>
            </html>
            """
        )
    )
    return {
        "root": tmp_path,
        "html": html,
        "css": css,
        "js": js,
        "svg": svg,
        "png": png,
    }


# utilities -----------------------------------------------------------


def _b64_in(html: str, mime: str) -> bool:
    return f"data:{mime};base64," in html


# regex-mode tests ----------------------------------------------------


def test_inline_everything_regex(tiny_site: dict[str, Path]) -> None:
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"])
    assert "<style>" in out
    assert "<script>" in out
    assert _b64_in(out, "image/png")
    assert _b64_in(out, "image/svg+xml")
    assert "<!-- begin 'style.css' -->" in out
    assert "<!-- end 'app.js' -->" in out


def test_indentation_preserved_2(tiny_site: dict[str, Path]) -> None:
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"])
    assert "\n    <style>" in out or "\n    <script>" in out


def test_max_bytes_limit(tiny_site: dict[str, Path]) -> None:
    big_js = tiny_site["root"] / "big.js"
    big_js.write_bytes(b"x" * 200_000)
    tiny_site["html"].write_text(
        tiny_site["html"]
        .read_text()
        .replace("</body>", '<script src="big.js"></script>\n</body>')
    )
    out = _inline(
        tiny_site["html"].read_text(),
        tiny_site["root"],
        {"max_bytes": 1_024},
    )
    assert '<script src="big.js"></script>' in out


def test_allowed_extensions_filter_2(tiny_site: dict[str, Path]) -> None:
    out = _inline(
        tiny_site["html"].read_text(),
        tiny_site["root"],
        {"allowed_extensions": {".css"}},
    )
    assert "<style>" in out
    assert '<script src="app.js">' in out
    assert not _b64_in(out, "image/png")


def test_comment_toggle_off(tiny_site: dict[str, Path]) -> None:
    out = _inline(
        tiny_site["html"].read_text(),
        tiny_site["root"],
        {"include_filename_comments": False},
    )
    assert "begin 'style.css'" not in out


def test_disable_local_and_remote(tiny_site: dict[str, Path]) -> None:
    out = _inline(
        tiny_site["html"].read_text(),
        tiny_site["root"],
        {"local": False, "remote": False},
    )
    assert 'href="style.css"' in out


# remote fetch --------------------------------------------------------


def test_remote_asset_inlined(
    monkeypatch: pytest.MonkeyPatch, tiny_site: dict[str, Path]
) -> None:
    remote_css = "https://cdn.example.com/remote.css"
    tiny_site["html"].write_text(
        tiny_site["html"].read_text().replace("style.css", remote_css)
    )

    class _Resp(io.BytesIO):
        def __enter__(self):  # type: ignore[override]
            return self

        def __exit__(self, *exc):  # type: ignore[override]
            pass

    def fake_open(url: str, *a, **k):  # type: ignore[override]
        assert url == remote_css
        return _Resp(b"body{background:blue;}")

    monkeypatch.setattr(urllib.request, "urlopen", fake_open)
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"], {"remote": True})
    assert "background:blue" in out


def test_remote_blocked(
    monkeypatch: pytest.MonkeyPatch, tiny_site: dict[str, Path]
) -> None:
    remote_css = "https://cdn.example.com/remote.css"
    tiny_site["html"].write_text(
        tiny_site["html"].read_text().replace("style.css", remote_css)
    )
    monkeypatch.setattr(urllib.request, "urlopen", lambda *a, **k: io.BytesIO(b""))
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"])
    assert f'href="{remote_css}"' in out


# bs4 parity ----------------------------------------------------------


def test_bs4_equals_regex(tiny_site: dict[str, Path]) -> None:
    raw = tiny_site["html"].read_text()
    out_regex = _inline(raw, tiny_site["root"])
    out_bs4 = _inline(raw, tiny_site["root"], {"use_bs4": True})
    assert "<style>" in out_bs4 and "<style>" in out_regex
    assert _b64_in(out_bs4, "image/png")
    assert "<!-- begin 'style.css' -->" in out_bs4


def test_bs4_prettify(tiny_site: dict[str, Path]) -> None:
    cfg = bundle_html.InlineConfig(use_bs4=True)
    pretty = bundle_html.inline_html_assets(
        tiny_site["html"].read_text(),
        base_path=tiny_site["root"],
        config=cfg,
        prettify=True,
    )
    assert pretty.lstrip().lower().startswith("<!doctype")


# tag-attr override ---------------------------------------------------


def test_custom_attribute_name(tiny_site: dict[str, Path]) -> None:
    tiny_site["html"].write_text(
        tiny_site["html"].read_text().replace("href", "data-href")
    )
    cfg = {"tag_attr": {"link": "data-href"}}
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"], cfg)
    assert "<style>" in out


# data-uri idempotence -----------------------------------------------


def test_data_uri_not_reprocessed(tiny_site: dict[str, Path]) -> None:
    # first inline to get data URIs
    once = _inline(tiny_site["html"].read_text(), tiny_site["root"])
    # second pass should leave them unchanged
    twice = _inline(once, tiny_site["root"])
    assert twice == once


# mixed quotes --------------------------------------------------------


def test_single_quotes_handled(tiny_site: dict[str, Path]) -> None:
    tiny_site["html"].write_text(
        tiny_site["html"]
        .read_text()
        .replace('"app.js"', "'app.js'")  # mix quote styles
    )
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"])
    assert "<script>" in out


# fragment ids --------------------------------------------------------


def test_fragment_in_src_kept(tiny_site: dict[str, Path]) -> None:
    # icon.svg#i should be replaced by a data URI but the #i fragment removed
    out = _inline(tiny_site["html"].read_text(), tiny_site["root"])
    assert "#i" not in out
    assert _b64_in(out, "image/svg+xml")


# CLI -----------------------------------------------------------------


def test_cli_overwrite(tmp_path: Path, tiny_site: dict[str, Path]) -> None:
    copy = tmp_path / "page.html"
    copy.write_text(tiny_site["html"].read_text())
    exe = Path(bundle_html.__file__).resolve()
    subprocess.check_call([sys.executable, str(exe), str(copy), "--output", str(copy)])
    res = copy.read_text()
    assert "<style>" in res
    assert _b64_in(res, "image/png")
