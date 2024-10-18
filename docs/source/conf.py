"""Configuration file for the Sphinx documentation builder."""

from importlib.metadata import version as _version

# Project information
project = 'sapimclient'
copyright = '2024, Niels Perfors'
author = 'Niels Perfors'
release = _version(project)
version = '.'.join(release.split('.')[:2])

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',  # https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
templates_path = ['_templates']
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

# Extensions configuration
autosectionlabel_prefix_document = True
autodoc_class_signature = 'separated'
autodoc_default_options = {
    'exclude-members': '__init__, __new__',
    'show-inheritance': True,
}
html_theme = 'sphinx_rtd_theme'
epub_show_urls = 'footnote'
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
