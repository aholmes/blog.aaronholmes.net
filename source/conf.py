import fnmatch
import os
import sys
import zipfile
from pathlib import Path

from docutils.nodes import Element
from sphinx.application import Sphinx

from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole

sys.path.append(str(Path('../lib/sphinx-tags/src').resolve()))
print(sys.path)

project = 'blog.aaronholmes.net'
copyright = '2025, Aaron Holmes'
author = 'Aaron Holmes'

master_doc = "index"

extensions: list[str] = []

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = []

html_theme = "sphinx_rtd_theme"
pygments_style = "one-dark"
html_static_path: list[str] = ["_static"]
html_css_files: list[str] = ["custom.css"]

tags_create_tags = True
tags_intro_text = ""
tags_page_title = ""
tags_index_head = "Tags"
tags_page_header = "Pages with this tag"

# https://github.com/uclahs-cds/Ligare/blob/2021ffdeac4b92cf726a8fc35866a069119cb788/sphinx-docs/source/conf.py

extensions: list[str] = [
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx_copybutton",
    "sphinx.ext.extlinks",
    "sphinxcontrib.plantuml",
    "sphinx_tags"
]


copybutton_exclude = ".linenos, .gp"
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

github_ref = os.environ.get("GITHUB_REF") or "main"

extlinks: dict[str, tuple[str, str|None]] = {
    "source": (
        f"https://github.com/aholmes/blog.aaronholmes.net/blob/{github_ref}/%s",
        None,
    ),
    "example": (
        f"https://github.com/aholmes/blog.aaronholmes.net/blob/{github_ref}/examples/%s",
        "Review example sources [%s]",
    ),
    "archive": (
        "https://blog.aaronholmes.net.github.io/aholmes/blog.aaronholmes.net/_downloads/%s.zip",
        "Download example archive [%s.zip]",
    )
}

plantuml = "docker run \
        -i \
        ghcr.io/uclahs-cds/plantuml-github-action:v2.0.0 \
        -DPLANTUML_LIMIT_SIZE=8192 \
        -v -p -tpng"


def create_zips_for_examples(app: Sphinx, exception: Exception | None):
    if exception is not None:
        return

    examples_dir = Path("examples").resolve()
    example_paths = examples_dir.glob("*")
    output_dir = Path(app.outdir, "_downloads")

    if not output_dir.exists():
        output_dir.mkdir()

    for example_path in example_paths:
        # Store the zip file in the `_downloads` output directory with the name
        # of the example (which is the directory name), e.g. _downloads/web-api.zip
        with zipfile.ZipFile(
            Path(output_dir, f"{example_path.name}.zip"), "w", zipfile.ZIP_DEFLATED
        ) as zip_file:
            for root, dirs, files in os.walk(examples_dir):
                # skip anything based on the Sphinx exclude_patterns list
                should_skip = any(
                    fnmatch.fnmatch(str(Path(root, _dir)), pat)
                    for _dir in dirs
                    for pat in exclude_patterns
                )

                if should_skip:
                    # ensures the loop won't look at directories in the skipped directory
                    dirs.clear()
                    continue

                for file in files:
                    file_path = Path(root, file)
                    arcname = Path.relative_to(file_path, examples_dir)
                    zip_file.write(file_path, arcname)

class TagXRefRole(XRefRole):
    def process_link(self, env: BuildEnvironment, refnode: Element, has_explicit_title: bool, title: str, target: str) -> tuple[str, str]:
        refnode["refdomain"] = "std"
        refnode["reftype"] = "ref"
        target = f"sphx_tag_{target}"
        return (title, target)

def setup(app: Sphinx) -> None:
    _ = app.add_role("tag", TagXRefRole())
    _ = app.connect("build-finished", create_zips_for_examples)
