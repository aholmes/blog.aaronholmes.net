import fnmatch
import html
import os
import re
import sys
import zipfile
from pathlib import Path
from typing import Any, TYPE_CHECKING, Callable
from datetime import datetime

from docutils.nodes import (
    Element,
    document as DocumentNode,
    meta as MetaNode,
    inline as InlineNode,
    raw as RawNode,
    system_message,
    Node
)
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx
from sphinx.environment import BuildEnvironment
from sphinx.roles import XRefRole
from enum import StrEnum

class BuildEnv(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

BUILD_ENV = (
    BuildEnv(BUILD_ENV_STR)
     if (BUILD_ENV_STR := os.getenv("BUILD_ENV")) in [e.value for e in BuildEnv]
     else BuildEnv.DEVELOPMENT
)

sys.path.append(str(Path('../lib/sphinx-tags/src').resolve()))
sys.path.append(str(Path('../lib/sphinx-conestack-theme').resolve()))

if TYPE_CHECKING:
    class PageDate(InlineNode, Element):
        ...
# TODO move the directive into its own module
sys.path.append(str(Path('../lib/pagedate').resolve()))
from pagedate import PageDate # pyright: ignore[reportMissingImports,reportUnknownVariableType]

project = "Bits, Bobs & Breakpoints \u2014 Aaron Holmes"
html_title = project
html_short_title = html_title
copyright = '2025, Aaron Holmes'
author = 'Aaron Holmes'
html_favicon = '_static/favicon.ico'
html_show_sphinx = False

master_doc = "index"

extensions: list[str] = []

templates_path: list[str] = ['_templates']
exclude_patterns: list[str] = []

html_theme = "conestack"
pygments_style = "one-dark"
html_static_path: list[str] = ["_static"]
html_extra_path: list[str] = ["ads.txt"]
html_css_files: list[str] = ["custom.css"]
html_theme_options = {
    "logo_url": "",
    "logo_title": project,
    "github_url": "https://github.com/aholmes/aaronholmes.net"
}

if BUILD_ENV == BuildEnv.DEVELOPMENT:
    html_baseurl = "/"
else:
    html_baseurl = "https://aaronholmes.net/"


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
    "sphinx_tags",
    "sphinx_reredirects",
    "sphinx_sitemap"
]


sitemap_url_scheme = "{link}"

# Old blog URLs.
# The index.html is used because CloudFlare munges the
# redirect URL to include it. Without it, Sphinx isn't
# able to build the old "fake" pages that are used for
# redirects.
redirects = {
    "2024-08-08_MakingACopperWireTree_BoutrosLab/index.html": "/2024/making_a_copper_wire_tree.html",
    "2022-09-22_WinterIsCanning_BoutrosLab/index.html": "/2022/winter_is_canning_2022.html",
    "2022-04-07_PairProgramming_BoutrosLab/index.html": "/2022/pair_programming.html",
    "2021-10-28_MyDogCleo_BoutrosLab/index.html": "/2021/my_dog_cleo.html",
    "2021-04-21_TypesInSoftware_BoutrosLab/index.html": "/2021/types_in_software.html",
    "displaying-response-headers-and-pretty-json-with-curl/index.html": "/2019/displaying_response_headers_and_pretty_json_with_curl.html",
    "the-behavior-of-c-nested-static-classes/index.html": "/2018/the_behavior_of_csharp_nested_static_classes.html",
    "transparent-video-in-all-browsers-from-cross-domain-sources/index.html": "/2017/transparent_video_in_all_browsers_from_cross_domain_sources.html",
    "using-git-with-git-directory-outside-the-git-repository/index.html": "/2016/using_git_with_the_git_directory_outside_the_git_repository_directory.html",
    "simple-way-to-prevent-website-jumping-from-scrollbars/index.html": "/2016/simple_way_to_prevent_websites_jumping_from_scrollbars.html",
    "two-short-ack-filetype-definitions-for-typescript/index.html": "/2016/two_short_ack_filetype_definitions_for_typescript.html",
    "simple-programming-patterns-and-conventions/index.html": "/2015/simple_programming_patterns_and_conventions.html",
    "printing-function-body-in-chromes-console/index.html": "/2015/printing_function_body_in_chromes_console.html",
    "reading-an-http-request-response-body-from-exceptions/index.html": "/2015/reading_an_http_request_response_body_from_exceptions.html",
    "circuit-scribe-art-project-step-3/index.html": "/2015/circuit_scribe_art_project_step_number_3.html",
    "circuit-scribe-art-project-step-2/index.html": "/2015/circuit_scribe_art_project_step_number_2.html",
    "circuit-scribe-art-project-step-1/index.html": "/2015/circuit_scribe_art_project_step_number_1.html",
    "writing-angularjs-directives-as-typescript-classes/index.html": "/2015/writing_angularjs_directives_as_typescript_classes.html",
    "using-time-as-a-color-generator/index.html": "/2014/using_time_as_a_color_generator.html",
    "speech-synthesis-on-windows-phone-8-1/index.html": "/2014/speech_synthesis_on_windows_phone_8_1.html",
    "my-ghost-theme-a-fork-of-casper/index.html": "/2014/my_ghost_theme_casper_for_developers.html",
    "running-entity-framework-migrations-on-application-start/index.html": "/2014/running_entity_framework_migrations_on_application_start.html",
    "displaying-code-with-ace-on-ghost/index.html": "/2014/displaying_code_with_ace_on_ghost.html",
    "canvas-vector-animations-with-css-or-javascript/index.html": "/2014/javascript_vector_animations_with_divs_or_canvas.html",
    "stack-your-circuit-scribe-modules/index.html": "https://www.instructables.com/Stack-your-Circuit-Scribe-modules",
    "astable-multivibrator-led-flasher-with-circuit-scribe/index.html": "https://www.instructables.com/Astable-microvibrator-LED-flasher-with-Circuit-Scr",
    "page/index.html": "/index.html",
    "page/1/index.html": "/index.html",
    "page/2/index.html": "/index.html",
    "page/3/index.html": "/index.html",
    "page/4/index.html": "/index.html",
    "page/5/index.html": "/index.html",
    "author/aaron/index.html": "/index.html"
}

copybutton_exclude = ".linenos, .gp"
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True
copybutton_only_copy_prompt_lines = True

github_ref = os.environ.get("GITHUB_REF") or "main"

extlinks: dict[str, tuple[str, str|None]] = {
    "source": (
        f"https://github.com/aholmes/aaronholmes.net/blob/{github_ref}/%s",
        None,
    ),
    "example": (
        f"https://github.com/aholmes/aaronholmes.net/blob/{github_ref}/examples/%s",
        "Review example sources [%s]",
    ),
    "archive": (
        "https://aholmes.github.io/aaronholmes.net/_downloads/%s.zip",
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

def get_time_node(
    date_raw: str,
    format: str = "%d %B %Y",
    transform: Callable[[str], str] | None = None):
    try:
        dt  = datetime.strptime(date_raw, "%Y-%m-%d")
        txt = dt.strftime(format).lstrip("0")
        if transform:
            txt = transform(txt)
    except ValueError:
        txt = date_raw

    return RawNode(
        '',
        f'<time class="page-date" datetime="{date_raw}">{txt}</time>',
        format='html'
    )

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

    html_time = get_time_node(date_raw, transform=lambda date_txt: date_txt.strip("0"))

    for node in doctree.traverse(PageDate):
        node.replace_self(html_time)

class DateRole(XRefRole):
    """
    Used like:
    :date:`2025-08-06`
    :date:`2025-08-06 <%Y-%m-%d>`

    Uses the default output format "%d %B %Y"
    Input format must be "%Y-%m-%d"
    """
    def run(self) -> tuple[list[Node], list[system_message]]:
        html_time = get_time_node(self.title, self.target)
        return [html_time], []

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
    _ = app.add_role("date", DateRole())
    _ = app.connect("build-finished", create_zips_for_examples)
    _ = app.connect("doctree-read", collect_meta_dates)
    _ = app.connect('html-page-context', add_dates_to_index_body)
    _ = app.connect("doctree-resolved", add_dates_to_page)