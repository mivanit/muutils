from pathlib import Path
import subprocess

from weasyprint import HTML as WeasyHTML  # type: ignore[import-untyped]


def html_to_pdf(src: Path, dst: Path) -> None:
    "write HTML file to PDF using WeasyPrint."
    WeasyHTML(filename=src.as_posix()).write_pdf(dst.as_posix())


def crop(pdf_in: Path, pdf_out: Path, margin_pt: int = 2) -> None:
    """Run pdfcrop with a tiny safety margin."""
    subprocess.run(
        ["pdfcrop", "--margins", str(margin_pt), pdf_in.as_posix(), pdf_out.as_posix()],
        check=True,
    )


def save_html_to_pdf(
    html: str,
    pdf_out: Path,
    pdfcrop: bool = True,
    margin_pt: int = 2,
) -> None:
    """Save HTML string to PDF file."""
    if isinstance(pdf_out, str):
        pdf_out = Path(pdf_out)
    temp_html: Path = pdf_out.with_suffix(".html")
    temp_html.write_text(html, encoding="utf-8")

    html_to_pdf(temp_html, pdf_out)

    if pdfcrop:
        crop(pdf_out, pdf_out, margin_pt)

    # Clean up temporary HTML file
    temp_html.unlink(missing_ok=True)
