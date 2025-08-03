import fnmatch
import html
import os
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, TYPE_CHECKING
from datetime import datetime

from docutils.nodes import (
    Element,
    document as DocumentNode,
    meta as MetaNode,
    inline as InlineNode,
    raw as RawNode
)
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole

sys.path.append(str(Path('../lib/sphinx-tags/src').resolve()))

if TYPE_CHECKING:
    class PageDate(InlineNode, Element):
        ...
sys.path.append(str(Path('../lib/pagedate').resolve()))
from pagedate import PageDate # pyright: ignore[reportMissingImports,reportUnknownVariableType]

project = "Aaron Holmes' thoughts"
html_title = project
html_short_title = html_title
copyright = '2025, Aaron Holmes'
author = 'Aaron Holmes'
html_favicon = '_static/favicon.ico'

master_doc = "index"

extensions: list[str] = []

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = []

html_theme = "piccolo_theme"
pygments_style = "one-dark"
html_static_path: list[str] = ["_static"]
html_css_files: list[str] = ["custom.css"]

html_theme_options: dict[str, Any] = {
    "globaltoc_collapse": False
}


tags_create_tags = True
tags_intro_text = ""
tags_page_title = "Tag"
tags_index_head = "Tags"
tags_page_header = "Pages with this tag"

# https://github.com/uclahs-cds/Ligare/blob/2021ffdeac4b92cf726a8fc35866a069119cb788/sphinx-docs/source/conf.py

extensions: list[str] = [
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx_copybutton",
    "sphinx.ext.extlinks",
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
        """
        A role to render sphinx_tags tags.
        """
        refnode["refdomain"] = "std"
        refnode["reftype"] = "ref"
        target = f"sphx_tag_{target}"
        return (title, target)


def collect_meta_dates(app: Sphinx, doctree: DocumentNode):
    """
    Extract `:date:` from `.. meta::` and set it in the page metadata.
    This lets `inject_dates_into_tocnodes` rewrite the TOC titles to include dates.
    """
    docname = app.env.docname
    for node in doctree.traverse(MetaNode):
        if node.get("name") == "date":
            app.env.metadata.setdefault(docname, {})["date"] = node["content"]


# <a class="reference internal" href="subdoc.html">Title</a>
rx = re.compile(r'(<a[^>]+href=")([^"]+)\.html(".*?>)([^<]+)(</a>)')
def add_dates_to_index_body(app: Sphinx, pagename: str, templatename: str, context: dict[str, Any], doctree: DocumentNode) -> str | None:
    """
    Insert a span containing the page's date (from metadata).
    """
    env = app.builder.env
    if not (body := context.get("body")):
        return

    def repl(m: re.Match[str]) -> str:
        href, doc, rest, text, tail = m.groups()

        pagename_path = Path(html.unescape(pagename))
        doc_name = str(Path(html.unescape(doc)))
        if not (doc_metadata := env.metadata.get(doc_name, {})):
            doc_metadata = env.metadata.get(str(Path(pagename_path.parent, doc_name)), {})

        date = doc_metadata.get("date")
        if not date:
            return m.group(0)

        new_text = f'<time class="toc-date" datetime="{date}">{date}</time>'
        return f"<span>{new_text}{href}{doc}.html{rest}{text}{tail}</span>"

    context["body"] = rx.sub(repl, body)


class PageDateDirective(Directive):
    """
    Add directive `.. pagedate::` that is replaced with the date from the page's metadata.
    """
    has_content = False
    def run(self):
        return [PageDate('')]


def add_dates_to_page(app: Sphinx, doctree: DocumentNode, docname: str):
    """
    Replace `.. pagedate::` with the appropriate HTML.
    """
    env = app.builder.env
    date_raw  = env.metadata.get(docname, {}).get('date')
    if not date_raw:
        for node in doctree.traverse(PageDate):
            node.replace_self([])
        return

    try:
        dt  = datetime.strptime(date_raw, "%Y-%m-%d")
        txt = dt.strftime("%d %B %Y").lstrip("0")
    except ValueError:
        txt = date_raw

    html_time = RawNode(
        '',
        f'<time class="page-date" datetime="{date_raw}">{txt}</time>',
        format='html'
    )

    for node in doctree.traverse(PageDate):
        node.replace_self(html_time)


rst_prolog = """
.. role:: underline
    :class: underline
.. role:: strike
    :class: strike
.. |pagedate| pagedate::
.. |cta| raw:: html

    <hr class="docutils">
    <span>Need additional help? Consider contacting me on <a href="https://www.codementor.io/@aholmes"><img src="https://cdn.codementor.io/badges/book_session_github.svg" alt="Book session on Codementor" style="display:inline;margin:0;vertical-align:middle;" /></a></span>
.. |disqus| raw:: html

    <div id="disqus_thread"></div>
    <script type="text/javascript">
        var disqus_shortname = 'aholmes';
        (function ()
        {
            var dsq = document.createElement('script'); dsq.type = 'text/javascript'; dsq.async = true;
            dsq.src = '//' + disqus_shortname + '.disqus.com/embed.js';
            (document.getElementsByTagName('head')[0] || document.getElementsByTagName('body')[0]).appendChild(dsq);
        })();
    </script>
"""


def setup(app: Sphinx) -> None:
    _ = app.add_node(PageDate)
    _ = app.add_directive("pagedate", PageDateDirective)
    _ = app.add_role("tag", TagXRefRole())
    _ = app.connect("build-finished", create_zips_for_examples)
    _ = app.connect("doctree-read", collect_meta_dates)
    _ = app.connect('html-page-context', add_dates_to_index_body)
    _ = app.connect("doctree-resolved", add_dates_to_page)
