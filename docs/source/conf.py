# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

from os import listdir
from os import mkdir
from shutil import copyfile

import pyrubrum

# -- Project information -----------------------------------------------------

FIGURE_TEMPLATE = """
Structure
---------

.. figure:: ../_static/flowcharts/{filename}.png

"""
EXAMPLE_TEMPLATE = """
{title}
{separators}

.. note::
    In order to make use of the proposed example, you need to
    set your own environment by creating a file named ``.env``
    and configuring all the variables from :doc:`sample.env <sample>`.

.. seealso::
    Check the :doc:`Flowchart guidelines <../flowchart>` to
    understand how the structure is built.

{figure}

Source code
-----------

.. literalinclude:: ../_static/examples/{filename}
"""
EXAMPLE_TITLES = {"cafe_bot.py": "Café Bot"}

FIGURES = {
    "cafe_bot.py": "cafe_bot",
    "calendar_bot.py": "calendar_bot",
    "hitchhiker_bot.py": "hitchhiker_bot",
    "sample_bot.py": "sample_bot",
}

project = pyrubrum.__package__
copyright = "2020, Hearot"
author = pyrubrum.__author__

root_files = ["CHANGELOG.md", "CODE_OF_CONDUCT.md", "README.md", "SECURITY.md"]
copies = root_files + ["FEATURES.md"]

for root_file in root_files:
    copyfile("../../" + root_file, root_file)

for root_file in copies:
    copyfile("../../" + root_file, "_static/" + root_file)

try:
    mkdir("examples/")
except (FileNotFoundError, OSError, PermissionError):
    pass


for example in filter(lambda f: f.endswith(".py"), listdir("../../examples")):
    copyfile("../../examples/" + example, "_static/examples/" + example)

    with open(
        "examples/" + example.replace(".py", ".rst"), "w", encoding="utf-8"
    ) as example_rst:
        if example in EXAMPLE_TITLES:
            title = EXAMPLE_TITLES[example]
        else:
            title = example.replace("_", " ").replace(".py", "").title()

        if example in FIGURES:
            figure = FIGURE_TEMPLATE.format(filename=FIGURES[example])
        else:
            figure = ""

        example_rst.write(
            EXAMPLE_TEMPLATE.lstrip().format(
                figure=figure,
                filename=example,
                title=title,
                separators="=" * len(title),
            )
        )

copyfile("../../examples/sample.env", "_static/examples/sample.env")

with open("README.md", "r", encoding="utf-8") as readme:
    content = readme.read().replace("./", "_static/")

with open("README.md", "w", encoding="utf-8") as readme:
    readme.write(content)

# The full version, including alpha/beta/rc tags
release = pyrubrum.__version__

napoleon_include_init_with_doc = False

# -- General configuration ---------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

default_role = "py:obj"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "m2r",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinx_rtd_theme",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

html_favicon = "_static/assets/pink_icon.ico"

html_logo = "_static/assets/mark_logo.png"

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

html_theme_options = {"style_nav_header_background": "pink"}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

intersphinx_mapping = {
    "pyrogram": ("https://docs.pyrogram.org/", None),
    "python": ("https://docs.python.org/3", None),
    "redis": ("https://redis-py.readthedocs.io/en/stable/", None),
}
