# -*- coding: utf-8 -*-
#
# PyGeoC documentation build configuration file, created by
# sphinx-quickstart on Thu Sep 14 15:34:26 2017.
#

import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import recommonmark
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

source_parsers = {
    '.md': CommonMarkParser
}

needs_sphinx = '1.5'
extensions = ['matplotlib.sphinxext.plot_directive',
              'sphinx.ext.inheritance_diagram',
              'sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.doctest',
              'sphinx.ext.todo',
              'sphinx.ext.mathjax',
              'sphinx.ext.napoleon']

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

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# source_encoding = 'utf-8'
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']
master_doc = 'index'

# General information about the project.
project = u'PyGeoC'
copyright = u'2016-2017, Liangjun Zhu'
author = u'Liangjun Zhu'
# Parse the version from the pygeoc module.
with open('../pygeoc/__init__.py') as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue
release = version

language = 'zh_CN'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = True

# -- Options for HTML output --
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for HTMLHelp output --
htmlhelp_basename = 'PyGeoCdoc'

# -- Options for LaTeX output --
latex_elements = {
}

latex_documents = [
    (master_doc, 'PyGeoC.tex', u'PyGeoC Documentation',
     u'Liangjun Zhu', 'manual'),
]

# -- Options for manual page output --
man_pages = [
    (master_doc, 'pygeoc', u'PyGeoC Documentation',
     [author], 1)
]

# -- Options for Texinfo output --
texinfo_documents = [
    (master_doc, 'PyGeoC', u'PyGeoC Documentation',
     author, 'PyGeoC', 'One line description of project.',
     'Miscellaneous'),
]

# app setup hook

github_doc_root = 'https://github.com/lreis2415/PyGeoC/tree/master/docs/'
def setup(app):
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)
