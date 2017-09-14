# -*- coding: utf-8 -*-
#
# PyGeoC documentation build configuration file, created by
# sphinx-quickstart on Thu Sep 14 15:34:26 2017.
#

import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import recommonmark
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

source_parsers = {
    '.md': CommonMarkParser
}

needs_sphinx = '1.5'
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.todo',
    'sphinx.ext.mathjax']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']
# source_encoding = 'utf-8'
# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst', '.md']
master_doc = 'index'

# General information about the project.
project = u'PyGeoC'
copyright = u'2017, Liang-Jun Zhu'
author = u'Liang-Jun Zhu'
github_doc_root = 'https://github.com/lreis2415/PyGeoC/tree/master/docs/'
version = u'0.1.2'
release = u'0.1.2'

language = 'en_US'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = True

# -- Options for HTML output --
html_title = u'PyGeoC 用户手册'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for HTMLHelp output --
htmlhelp_basename = 'PyGeoCdoc'

# -- Options for LaTeX output --
latex_elements = {
}

latex_documents = [
    (master_doc, 'PyGeoC.tex', u'PyGeoC Documentation',
     u'Liang-Jun Zhu', 'manual'),
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
def setup(app):
    app.add_config_value('recommonmark_config', {
        'url_resolver': lambda url: github_doc_root + url,
        'auto_toc_tree_section': 'Contents',
        'enable_eval_rst': True,
        'enable_auto_doc_ref': True,
    }, True)
    app.add_transform(AutoStructify)


