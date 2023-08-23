# -*- coding: utf-8 -*-
# flake8: noqa: E402
# pylint: disable=redefined-builtin,wrong-import-position
"""Configuration file for the Sphinx documentation builder.

This file does only contain a selection of the most common options. For a
full list see the documentation:
http://www.sphinx-doc.org/en/master/config
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
import os
import sys
sys.path.insert(0, os.path.abspath("../../src"))
myself = __import__("solo")
PY2 = (sys.version_info[0] == 2)

# -- Project information -----------------------------------------------------

project = myself.__name__.rsplit(".", 1)[-1]
copyright = " 2017-2019, 2023 Víctor Molina García"
author = "Víctor Molina García"

# The short X.Y version
version = ""
# The full version, including alpha/beta/rc tags
release = myself.__version__


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

autodoc_default_options = {
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

autosummary_generate = True
autosummary_generate_overwrite = False
napoleon_use_ivar = True
napoleon_use_rtype = False
intersphinx_mapping = {
    "python":
        ("https://docs.python.org/3", None),
    "numpy":
        ("https://numpy.org/doc/stable/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = [".rst", ".md"]
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "furo"
html_context = {}

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``["localtoc.html", "relations.html", "sourcelink.html",
# "searchbox.html"]``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "{0}doc".format(project)


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ("letterpaper" or "a4paper").
    "papersize": "letterpaper",
    # The font size ("10pt", "11pt" or "12pt").
    "pointsize": "10pt",
    # Additional stuff for the LaTeX preamble.
    "preamble": "",
    # Latex figure (float) alignment
    "figure_align": "htbp",
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [(
    master_doc,
    "{0}.tex".format(project),
    "{0} Documentation".format(project),
    author,
    "manual",
)]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(
    master_doc,
    project,
    "{0} Documentation".format(project),
    [author],
    1,
)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [(
    master_doc,
    project,
    "{0} Documentation".format(project),
    author,
    project,
    myself.__doc__,
    "Miscellaneous",
)]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ""

# A unique identification for the text.
#
# epub_uid = ""

# A list of files that should not be packed into the epub file.
epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# Replace the default `ClassDocumenter` so that the class members appear in
# the same order as in their files.
#
from sphinx.ext import autodoc
from sphinx.ext.autodoc import ClassDocumenter


class OrderedClassDocumenter(ClassDocumenter):
    """Specialised Documenter subclass for classes with ordered members."""

    def get_object_members(self, want_all):
        """Return list of pairs ``(name, member)`` from ``self.object``.

        Parameters
        ----------

        want_all : bool
            if ``want_all`` is True, return all members; otherwise,
            return only those members given by ``self.options.members``
            (which may also be None)

        Returns
        -------

        members_check_module : bool
            if True, the documentation will be generated only if the
            object is defined in the module name it is imported from

        members : list
            a list of pairs ``(name, member)`` for every member from
            ``self.object``
        """

        # Call the parent method.
        parent = super(OrderedClassDocumenter, self)
        members_check_module, members = parent.get_object_members(want_all)

        # Define custom sorter.
        def keysorter(item):
            """Return file line number for the given item."""
            _name, obj = item
            try:
                code = obj.im_func.func_code if PY2 else obj.__code__
            except AttributeError:
                return 0
            return code.co_firstlineno

        # Resort members based on their file line number and return.
        members.sort(key=keysorter)
        return members_check_module, members


autodoc.ClassDocumenter = OrderedClassDocumenter
