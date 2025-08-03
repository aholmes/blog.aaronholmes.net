# aaronholmes.net

This repository contains reStructuredText-formatted blog-style posts for [aaronholmes.net](https://aaronholmes.net).

# Technology

This repository uses Sphinx to compile reStructuredText to HTML.

The files published to https://aholmes.github.io/blog.aaronholmes.net.

The domain name aaronholmes.net contains a CNAME, A, and AAAA records for the GitHub website.

DNS is controlled through CloudFlare, along with various URL rewrite rules to handle migrating from my old Ghost-based website.

# Building

You must have [uv](https://docs.astral.sh/uv/) on your system.

The site can be compiled with `make html` or `make autobuild`.