from pathlib import Path
import argparse
import warnings
import tomllib

import pdoc
import pdoc.render

OUTPUT_DIR: Path = Path("docs")


def ignore_warnings():
    # Read the pyproject.toml file
    pyproject_path: Path = Path("pyproject.toml")
    with pyproject_path.open("rb") as f:
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
    parsed_args = argparser.parse_args()

    if not parsed_args.warn_all:
        ignore_warnings()

    pdoc.render.configure(
        edit_url_map={
            "muutils": "https://github.com/mivanit/muutils/blob/main/muutils/",
        },
        template_directory=Path("docs/templates/html/"),
        show_source=True,
        math=True,
        mermaid=True,
        search=True,
    )

    pdoc.pdoc(
        "muutils",
        output_directory=OUTPUT_DIR,
    )

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
