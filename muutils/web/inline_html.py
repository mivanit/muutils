"Inline local CSS/JS files into an HTML document"

from __future__ import annotations

from typing import Literal
from pathlib import Path
import warnings

AssetType = Literal["script", "style"]


def inline_html_assets(
    html: str,
    assets: list[tuple[AssetType, Path]],
    base_path: Path,
    include_filename_comments: bool = True,
    prettify: bool = False,
) -> str:
    """Inline specified local CSS/JS files into the text of an HTML document.

    Each entry in `assets` should be a tuple like `("script", "app.js")` or `("style", "style.css")`.

    # Parameters:
    - `html : str`
            input HTML content.
    - `assets : list[tuple[AssetType, Path]]`
            List of (tag_type, filename) tuples to inline.

    # Returns:
    `str` : Modified HTML content with inlined assets.
    """
    for tag_type, filename in assets:
        fname_str: str = filename.as_posix()
        if tag_type not in AssetType.__args__:  # type: ignore[attr-defined]
            err_msg: str = f"Unsupported tag type: {tag_type}"
            raise ValueError(err_msg)

        # Dynamically create the pattern for the given tag and filename
        pattern: str
        if tag_type == "script":
            pattern = rf'<script src="{fname_str}"></script>'
        elif tag_type == "style":
            pattern = rf'<link rel="stylesheet" href="{fname_str}">'
        # assert it's in the text exactly once
        assert (
            html.count(pattern) == 1
        ), f"Pattern {pattern} should be in the html exactly once, found {html.count(pattern) = }"
        # figure out the indentation level of the pattern  in the html
        indentation: str = html.split(pattern)[0].splitlines()[-1]
        assert (
            indentation.strip() == ""
        ), f"Pattern '{pattern}' should be alone in its line, found {indentation = }"
        # read the content and create the replacement
        content: str = (base_path / filename).read_text()
        replacement: str = f"<{tag_type}>\n{content}\n</{tag_type}>"
        if include_filename_comments:
            replacement = f"<!-- begin '{fname_str}' -->\n{replacement}\n<!-- end '{fname_str}' -->"
        # indent the replacement
        replacement = "\n".join(
            [f"{indentation}\t{line}" for line in replacement.splitlines()]
        )
        # perform the replacement
        html = html.replace(pattern, replacement)

    if prettify:
        try:
            from bs4 import BeautifulSoup

            soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
            # TYPING: .prettify() might return a str or bytes, but we want str?
            html = str(soup.prettify())
            print(BeautifulSoup)
        except ImportError:
            warnings.warn(
                "BeautifulSoup is not installed, skipping prettification of HTML."
            )

    return html


def inline_html_file(
    html_path: Path,
    output_path: Path,
    include_filename_comments: bool = True,
    prettify: bool = False,
) -> None:
    "given a path to an HTML file, inline the local CSS/JS files into it and save it to output_path"
    base_path: Path = html_path.parent
    # read the HTML file
    html: str = html_path.read_text()
    # read the assets
    assets: list[tuple[AssetType, Path]] = []
    for asset in base_path.glob("*.js"):
        assets.append(("script", Path(asset.name)))
    for asset in base_path.glob("*.css"):
        assets.append(("style", Path(asset.name)))
    # inline the assets
    html_new: str = inline_html_assets(
        html,
        assets,
        base_path,
        include_filename_comments=include_filename_comments,
        prettify=prettify,
    )
    # write the new HTML file
    output_path.write_text(html_new)


if __name__ == "__main__":
    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Inline local CSS/JS files into an HTML document."
    )
    parser.add_argument(
        "-i",
        "--input-path",
        type=Path,
        help="Path to the HTML file to process.",
    )
    parser.add_argument(
        "-o",
        "--output-path",
        type=str,
        help="Path to save the modified HTML file.",
    )

    parser.add_argument(
        "-c",
        "--no-filename-comments",
        action="store_true",
        help="don't include comments with the filename in the inlined assets",
    )

    parser.add_argument(
        "-p",
        "--no-prettify",
        action="store_true",
        help="don't prettify the HTML file",
    )

    args: argparse.Namespace = parser.parse_args()

    inline_html_file(
        html_path=Path(args.input_path),
        output_path=Path(args.output_path),
        include_filename_comments=not args.no_filename_comments,
        prettify=not args.no_prettify,
    )
