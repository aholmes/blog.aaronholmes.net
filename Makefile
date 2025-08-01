VENV ?= .venv
ACTIVATE_VENV := . $(VENV)/bin/activate

$(VENV):
	uv sync

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help: $(VENV)
	@$(ACTIVATE_VENV) && \
	$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile autobuild

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: $(VENV) Makefile
	@$(ACTIVATE_VENV) && \
	$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

autobuild: $(VENV) Makefile
	@$(ACTIVATE_VENV) && \
	sphinx-autobuild "$(SOURCEDIR)" "$(BUILDDIR)/html" \
		--ignore "$(SOURCEDIR)/_tags" \
		-j auto

clean:
	rm -rf "$(BUILDDIR)" "$(VENV)"