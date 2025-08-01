# this is a module because Sphinx needs to be able
# to import it due to pickling.

from docutils import nodes
# Used to denote `.. pagedate::` directives
class PageDate(nodes.inline, nodes.Element):
    pass