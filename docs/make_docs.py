from pathlib import Path
import argparse
import warnings
import tomllib
import inspect


import pdoc
import pdoc.render
import pdoc.doc
import pdoc.extract
import pdoc.render_helpers
from markupsafe import Markup

OUTPUT_DIR: Path = Path("docs")


def format_signature(sig: inspect.Signature, colon: bool) -> str:
    """Format a function signature for Markdown. Returns a single-line Markdown string."""
    # First get a list with all params as strings.
    result = pdoc.doc._PrettySignature._params(sig)  # type: ignore
    return_annot = pdoc.doc._PrettySignature._return_annotation_str(sig)  # type: ignore

    def _format_param(param: str) -> str:
        """Format a parameter for Markdown, including potential links."""
        # This is a simplified version. You might need to adjust this
        # to properly handle links in your specific use case.
        return f"`{param}`"

    # Format each parameter
    pretty_result = [_format_param(param) for param in result]

    # Join parameters
    params_str = ", ".join(pretty_result)

    # Add return annotation
    anno = ")"
    if return_annot:
        anno += f" -> `{return_annot}`"
    if colon:
        anno += ":"

    # Construct the full signature
    rendered = f"`(`{params_str}`{anno}`"

    return rendered


HTML_TO_MD_MAP: dict[str, str] = {
    "&gt;": ">",
    "&lt;": "<",
    "&amp;": "&",
    "&quot;": '"',
    "&#39": "'",
    "&apos;": "'",
}


def markup_safe(sig: inspect.Signature) -> str:
    output: str = str(sig)
    return Markup(output)


def use_markdown_format():
    pdoc.render_helpers.format_signature = format_signature
    pdoc.render.env.filters["markup_safe"] = markup_safe


def pdoc_combined(*modules: Path | str, output_file: Path) -> None:
    """Render the documentation for a list of modules into a single HTML file.

    Args:
        *modules: Paths or names of the modules to document.
        output_file: Path to the output HTML file.

    This function will:
    1. Extract all modules and submodules.
    2. Generate documentation for each module.
    3. Combine all module documentation into a single HTML file.
    4. Write the combined documentation to the specified output file.

    Rendering options can be configured by calling `pdoc.render.configure` in advance.
    """
    # Extract all modules and submodules
    all_modules: dict[str, pdoc.doc.Module] = {}
    for module_name in pdoc.extract.walk_specs(modules):
        all_modules[module_name] = pdoc.doc.Module.from_name(module_name)

    # Generate HTML content for each module
    module_contents: list[str] = []
    for module in all_modules.values():
        module_html = pdoc.render.html_module(module, all_modules)
        module_contents.append(module_html)

    # Combine all module contents
    combined_content = "\n".join(module_contents)

    # Write the combined content to the output file
    with output_file.open("w", encoding="utf-8") as f:
        f.write(combined_content)


def ignore_warnings(config_path: str | Path = Path("pyproject.toml")):
    # Read the pyproject.toml file
    config_path = Path(config_path)
    with config_path.open("rb") as f:
        pyproject_data = tomllib.load(f)

    # Extract the warning messages from the tool.pdoc.ignore section
    warning_messages: list[str] = (
        pyproject_data.get("tool", {}).get("pdoc", {}).get("warnings_ignore", [])
    )

    # Process and apply the warning filters
    for message in warning_messages:
        warnings.filterwarnings("ignore", message=message)


if __name__ == "__main__":
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    # whether to start an HTTP server to serve the documentation
    argparser.add_argument(
        "--serve",
        "-s",
        action="store_true",
        help="Whether to start an HTTP server to serve the documentation",
    )
    argparser.add_argument(
        "--warn-all",
        "-w",
        action="store_true",
        help="Whether to show all warnings, instead of ignoring the ones specified in pyproject.toml:tool.pdoc.ignore",
    )
    argparser.add_argument(
        "--combined",
        "-c",
        action="store_true",
        help="Whether to combine the documentation for multiple modules into a single markdown file",
    )
    parsed_args = argparser.parse_args()

    if not parsed_args.warn_all:
        ignore_warnings()

    pdoc.render.configure(
        edit_url_map={
            "muutils": "https://github.com/mivanit/muutils/blob/main/muutils/",
        },
        template_directory=Path("docs/templates/html/")
        if not parsed_args.combined
        else Path("docs/templates/markdown/"),
        show_source=True,
        math=True,
        mermaid=True,
        search=True,
    )

    if not parsed_args.combined:
        pdoc.pdoc(
            "muutils",
            output_directory=OUTPUT_DIR,
        )
    else:
        use_markdown_format()
        pdoc_combined("muutils", output_file=OUTPUT_DIR / "combined" / "muutils.md")

    if parsed_args.serve:
        import os
        import http.server
        import socketserver

        port: int = 8000
        os.chdir(OUTPUT_DIR)
        with socketserver.TCPServer(
            ("", port), http.server.SimpleHTTPRequestHandler
        ) as httpd:
            print(f"Serving at http://localhost:{port}")
            httpd.serve_forever()
