"Create publications markdown file"

import re
from pathlib import Path

import pybtex
from pybtex.style.formatting.unsrt import Style
from pybtex.style.formatting import toplevel

from pybtex.style.template import (
    words,
    field,
    optional,
    sentence,
    tag,
    optional_field,
)

date = words[optional_field("month"), field("year")]


def main():
    working_directory = Path("./")
    bibtex_folder = working_directory / "bibtex_input"
    md_path = working_directory / "README.md"

    new_style = NewStyle

    engine = pybtex.PybtexEngine()

    md = {}
    pub_types = ["papers", "preprints", "chapters", "software"]
    for pub_type in pub_types:
        bibtex_path = bibtex_folder / f"wvg_{pub_type}.bib"
        md[pub_type] = engine.format_from_files(
            [bibtex_path], style=new_style, output_backend="markdown"
        )

        md[pub_type] = put_bullet_points(md[pub_type])

    output = f"""
# Publications by Werner Van Geit


## Papers

{md['papers']}

## Preprints

{md['preprints']}

## Book chapters

{md['chapters']}

## Software

{md['software']}

    """

    # -- write down markdown wiki -- #
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(output)


class NewStyle(Style):
    """Style similar to unsrt, but with bold titles and sorting by date."""

    def format_title(self, e, which_field, as_sentence=True):
        formatted_title = field(
            which_field, apply_func=lambda text: text.capitalize()
        )
        formatted_title = tag("b")[formatted_title]
        if as_sentence:
            return sentence[formatted_title]
        else:
            return formatted_title

    def format_software(self, e):
        template = toplevel[
            optional[sentence[self.format_names("author")]],
            optional[self.format_title(e, "title")],
            sentence[
                optional[field("howpublished")],
                optional[date],
            ],
            sentence(capfirst=False)[optional_field("note")],
            self.format_web_refs(e),
        ]
        return template.format_data(e)


def put_bullet_points(input):
    """Replace references by bullet points."""
    to_replace = r"\[[0-9]+\]"
    return re.sub(to_replace, "\n*", input)


if __name__ == "__main__":
    main()
