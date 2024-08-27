from pathlib import Path

import pdoc
import pdoc.render

if __name__ == "__main__":
    pdoc.render.configure(
        edit_url_map={
            "muutils": "https://github.com/mivanit/muutils/blob/main/muutils/",
        },
        template_directory=Path("docs/templates"),
        show_source=True,
        math=True,
        mermaid=True,
        search=True,
    )

    pdoc.pdoc(
        "muutils",
        output_directory=Path("docs"),
    )