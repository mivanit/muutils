"""
Inline / bundle external assets (CSS, JS, SVG, PNG) into an HTML document.

Default mode uses **zero external dependencies** and a few well-targeted
regular expressions.  If you install *beautifulsoup4* you can enable the
far more robust BS4 mode by passing `InlineConfig(use_bs4=True)`.
"""

from __future__ import annotations

import base64
import re
import urllib.request
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Literal

# bs4 import deferred to avoid an unconditional dependency.

# constants
# ---------------------------------------------------------------------

AssetExt = Literal[".css", ".js", ".svg", ".png"]

DEFAULT_ALLOWED_EXTENSIONS: Final[set[AssetExt]] = {".css", ".js", ".svg", ".png"}

DEFAULT_TAG_ATTR: Final[dict[str, str]] = {
    "link": "href",  # <link rel="stylesheet" href="...">
    "script": "src",  # <script src="..."></script>
    "img": "src",  # <img src="...">
    "use": "xlink:href",  # <use xlink:href="sprite.svg#id">
}

MIME_BY_EXT: Final[dict[AssetExt, str]] = {
    ".css": "text/css",
    ".js": "application/javascript",
    ".svg": "image/svg+xml",
    ".png": "image/png",
}

# Configuration
# ---------------------------------------------------------------------


@dataclass
class InlineConfig:
    """High-level configuration for the inliner.

    # Parameters
    - `allowed_extensions : set[AssetExt]`
        Extensions that may be inlined.
    - `tag_attr : dict[str, str]`
        Mapping *tag -> attribute* that holds the asset reference.
    - `max_bytes : int`
        Assets larger than this are ignored.
    - `local : bool`
        Allow local filesystem assets.
    - `remote : bool`
        Allow remote http/https assets.
    - `include_filename_comments : bool`
        Surround every replacement with `<!-- begin '...' -->`
        and `<!-- end '...' -->`.
    - `use_bs4 : bool`
        Parse the document with BeautifulSoup if available.
    """

    allowed_extensions: set[AssetExt] = field(
        default_factory=lambda: set(DEFAULT_ALLOWED_EXTENSIONS)
    )
    tag_attr: dict[str, str] = field(default_factory=lambda: dict(DEFAULT_TAG_ATTR))
    max_bytes: int = 128 * 1024
    local: bool = True
    remote: bool = False
    include_filename_comments: bool = True
    use_bs4: bool = False


# Low-level helpers
# ---------------------------------------------------------------------


def _is_remote(url: str) -> bool:
    """Return *True* if *url* starts with http:// or https://."""
    return url.lower().startswith(("http://", "https://"))


def _fetch_bytes(src: str, base: Path) -> bytes:
    """Fetch *src* (local or remote) and return its raw bytes."""
    if _is_remote(src):
        with urllib.request.urlopen(src) as resp:
            return resp.read()
    return (base / src).read_bytes()


def _decode_text(buf: bytes) -> str:
    """Decode *buf* as UTF-8, falling back to replacement."""
    try:
        return buf.decode()
    except UnicodeDecodeError:
        return buf.decode("utf-8", "replace")


# Regex-based implementation (no deps)
# ---------------------------------------------------------------------


def _apply_indent(html: str, start: int, replacement: str) -> str:
    """Indent *replacement* to match the line that starts at *start*."""
    line_start: int = html.rfind("\n", 0, start) + 1
    indent: str = html[line_start:start]
    return "\n".join(indent + line for line in replacement.splitlines())


def _inline_with_regex(html: str, base: Path, cfg: InlineConfig) -> str:
    """Inline assets using pure-regex parsing (no third-party libs)."""
    tag: str
    attr: str
    for tag, attr in cfg.tag_attr.items():
        pattern: str
        if tag == "script":
            pattern = (
                rf"<script\b[^>]*\s{attr}\s*=\s*['\"]([^'\"]+)['\"][^>]*>\s*</script>"
            )
        elif tag == "link":
            pattern = rf"<link\b[^>]*\s{attr}\s*=\s*['\"]([^'\"]+)['\"][^>]*>"
        else:  # img, use, etc.
            pattern = rf"<{tag}\b[^>]*\s{attr}\s*=\s*['\"]([^'\"]+)['\"][^>]*>"

        matches: list[re.Match[str]] = list(re.finditer(pattern, html, re.IGNORECASE))
        m: re.Match[str]
        for m in reversed(matches):
            raw_src: str = m.group(1)  # may contain #fragment
            clean_src: str = re.split(r"[?#]", raw_src, maxsplit=1)[0]  # file path only
            ext: str = Path(clean_src).suffix.lower()

            if ext not in cfg.allowed_extensions:
                continue
            if _is_remote(clean_src) and not cfg.remote:
                continue
            if not _is_remote(clean_src) and not cfg.local:
                continue

            try:
                data: bytes = _fetch_bytes(clean_src, base)
            except Exception as err:
                warnings.warn(f"skip '{raw_src}': {err}")
                continue

            if len(data) > cfg.max_bytes:
                continue

            # build replacement
            replacement: str
            if ext in {".css", ".js"}:
                tag_name: str = "style" if ext == ".css" else "script"
                replacement = f"<{tag_name}>\n{_decode_text(data)}\n</{tag_name}>"
            else:  # .svg or .png
                b64: str = base64.b64encode(data).decode()
                # TYPING: we check earlier, ext if for sure in MIME_BY_EXT
                data_uri: str = f"data:{MIME_BY_EXT[ext]};base64,{b64}"  # type: ignore[index]
                replacement = m.group(0).replace(raw_src, data_uri, 1)

            if cfg.include_filename_comments:
                replacement = f"<!-- begin '{clean_src}' -->\n{replacement}\n<!-- end '{clean_src}' -->"

            replacement = _apply_indent(html, m.start(), replacement)
            html = html[: m.start()] + replacement + html[m.end() :]

    return html


# BeautifulSoup-based implementation (optional)
# ---------------------------------------------------------------------


def _inline_with_bs4(html: str, base: Path, cfg: InlineConfig) -> str:
    """Inline assets using BeautifulSoup when available."""
    try:
        from bs4 import BeautifulSoup, Comment, Tag
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise RuntimeError("BeautifulSoup requested but not installed") from exc

    soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

    tag: Tag  # TYPING: i think soup.find_all() returns a list of Tag objects? mypy thinks it should be PageElement (of which Tag is a subclass)
    for tag in list(soup.find_all(cfg.tag_attr.keys())):  # type: ignore[assignment]
        attr: str = cfg.tag_attr[tag.name]
        # TYPING: error: Incompatible types in assignment (expression has type "str | AttributeValueList | None", variable has type "str | None")  [assignment]
        src_full: str | None = tag.get(attr)  # type: ignore[assignment]
        if not src_full:
            continue

        clean_src: str = re.split(r"[?#]", src_full, 1)[0]
        ext: str = Path(clean_src).suffix.lower()

        if ext not in cfg.allowed_extensions:
            continue
        if _is_remote(clean_src) and not cfg.remote:
            continue
        if not _is_remote(clean_src) and not cfg.local:
            continue

        try:
            data: bytes = _fetch_bytes(clean_src, base)
        except Exception as err:
            warnings.warn(f"skip '{src_full}': {err}")
            continue

        if len(data) > cfg.max_bytes:
            continue

        if ext in {".css", ".js"}:
            new_tag: Tag = soup.new_tag("style" if ext == ".css" else "script")
            new_tag.string = _decode_text(data)
            if cfg.include_filename_comments:
                tag.insert_before(Comment(f" begin '{src_full}' "))
                tag.insert_after(Comment(f" end '{src_full}' "))
            tag.replace_with(new_tag)
        else:  # .svg or .png
            b64: str = base64.b64encode(data).decode()
            # we are sure ext is in MIME_BY_EXT, so ignore type error
            tag[attr] = f"data:{MIME_BY_EXT[ext]};base64,{b64}"  # type: ignore[index]
            if cfg.include_filename_comments:
                tag.insert_before(Comment(f" begin '{src_full}' "))
                tag.insert_after(Comment(f" end '{src_full}' "))

    return str(soup)


# Public API
# ---------------------------------------------------------------------


def inline_html_assets(
    html: str,
    *,
    base_path: Path,
    config: InlineConfig | None = None,
    prettify: bool = False,  # kept for API compatibility (ignored in regex mode)
) -> str:
    """Inline permitted external assets inside *html*.

    # Parameters
    - `html : str`
        Raw HTML text.
    - `base_path : Path`
        Directory used to resolve relative asset paths.
    - `config : InlineConfig | None`
        Inlining options (see `InlineConfig`).
    - `prettify : bool`
        Pretty-print output (only effective in BS4 mode).

    # Returns
    - `str`
        Modified HTML.
    """
    cfg: InlineConfig = config or InlineConfig()
    if cfg.use_bs4:
        html_out: str = _inline_with_bs4(html, base_path, cfg)
        if prettify:
            # lazy import to avoid unconditional dependency
            from bs4 import BeautifulSoup

            # TYPING: .prettify() returns str if no encoding is set
            html_out = str(BeautifulSoup(html_out, "html.parser").prettify())
    else:
        html_out = _inline_with_regex(html, base_path, cfg)
    return html_out


def inline_html_file(
    html_path: Path,
    output_path: Path,
    base_path: Path | None = None,
    config: InlineConfig | None = None,
    prettify: bool = False,
) -> Path:
    """Read *html_path*, inline its assets, and write the result.

    # Parameters
    - `html_path : Path`
        Source HTML file.
    - `output_path : Path`
        Destination path to write the modified HTML.
    - `base_path : Path | None`
        Directory used to resolve relative asset paths (defaults to the HTML file's directory).
        If `None`, uses the directory of *html_path*.
        (default: `None` -> use `html_path.parent`)
    - `config : InlineConfig | None`
        Inlining options.
        If `None`, uses default configuration.
        (default: `None` -> use `InlineConfig()`)
    - `prettify : bool`
        Pretty-print when `use_bs4=True`.
        (default: `False`)

    # Returns
    - `Path`
        Path actually written.
    """
    if base_path is None:
        base_path = html_path.parent
    html_raw: str = html_path.read_text()
    html_new: str = inline_html_assets(
        html_raw,
        base_path=base_path,
        config=config,
        prettify=prettify,
    )
    dest: Path = output_path or html_path
    dest.write_text(html_new)
    return dest


# CLI
# ---------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Inline / bundle CSS, JS, SVG, PNG assets. "
        "Uses regex parsing by default; pass --bs4 to require BeautifulSoup."
    )
    parser.add_argument("html", type=Path, help="input HTML file")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="output file",
        required=True,
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=None,
        help="base directory for relative asset paths (defaults to the HTML file's directory)",
    )
    parser.add_argument("--remote", action="store_true", help="allow remote URLs")
    parser.add_argument("--bs4", action="store_true", help="use BeautifulSoup parser")
    parser.add_argument(
        "--prettify", action="store_true", help="pretty-print with BeautifulSoup)"
    )
    parser.add_argument(
        "--max-bytes", type=int, default=128 * 1024, help="size limit per asset"
    )
    parser.add_argument(
        "--ext",
        nargs="+",
        default=list(DEFAULT_ALLOWED_EXTENSIONS),
        help="extensions to inline",
    )
    parser.add_argument(
        "--tag-attr",
        type=str,
        default=None,
        help='override tag->attr map. format: "tag1=attr1,tag2=attr2"',
    )
    parser.add_argument("--no-comments", dest="comments", action="store_false")
    args: argparse.Namespace = parser.parse_args()

    tag_attr: dict[str, str]
    if args.tag_attr:
        tag_attr = {
            tag: attr
            for tag, attr in (item.split("=") for item in args.tag_attr.split(","))
        }

    else:
        tag_attr = dict(DEFAULT_TAG_ATTR)

    cfg: InlineConfig = InlineConfig(
        allowed_extensions=set(args.ext),  # type: ignore[arg-type]
        tag_attr=tag_attr,
        max_bytes=args.max_bytes,
        remote=args.remote,
        include_filename_comments=args.comments,
        use_bs4=args.bs4,
    )

    inline_html_file(
        args.html,
        output_path=args.output,
        base_path=args.source_dir,
        config=cfg,
        prettify=args.prettify,
    )
