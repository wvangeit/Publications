"Create publications markdown file"

import re
from pathlib import Path

import pybtex
import pybtex.style.formatting.unsrt as pybtex_unsrt
import pybtex.style.template as pybtex_template


def main():
    working_directory = Path("./")
    bibtex_folder = working_directory / "bibtex_input"
    md_path = working_directory / "README.md"

    papers_path = bibtex_folder / "papers.bib"  # from zotero

    new_style = NewStyle

    engine = pybtex.PybtexEngine()

    md_papers = engine.format_from_files(
        [papers_path], style=new_style, output_backend="markdown"
    )

    md_papers = put_bullet_points(md_papers)

    output = f"""
# Publications by Werner Van Geit

## Scientific papers

{md_papers}
    """

    # -- write down markdown wiki -- #
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(output)


class NewStyle(pybtex_unsrt.Style):
    """Style similar to unsrt, but with bold titles and sorting by date."""

    def format_title(self, e, which_field, as_sentence=True):
        formatted_title = pybtex_template.field(
            which_field, apply_func=lambda text: text.capitalize()
        )
        formatted_title = pybtex_template.tag("b")[formatted_title]
        if as_sentence:
            return pybtex_template.sentence[formatted_title]
        else:
            return formatted_title


def put_bullet_points(input):
    """Replace references by bullet points."""
    to_replace = r"\[[0-9]+\]"
    return re.sub(to_replace, "*", input)


if __name__ == "__main__":
    main()
