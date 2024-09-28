"""Configuration file for the Sphinx documentation builder."""
# pylint: disable=all
from importlib.metadata import version


# Project information
project = "python-sapcommissions"
copyright = "2024, Niels Perfors"
author = "Niels Perfors"
release = version(project)
version = '.'.join(release.split('.')[:2])

# General configuration
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]
templates_path = ["_templates"]

# Options for HTML output
html_theme = "sphinx_rtd_theme"

# Options for EPUB output
epub_show_urls = "footnote"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True
