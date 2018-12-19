# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Standard Library
import os
import sys

PATH=os.path.normpath(os.path.join(os.path.dirname(__file__), "../src"))
sys.path.insert(0, PATH)


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.coverage',
    'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    'sphinx.ext.ifconfig',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
]
if os.getenv('SPELLCHECK'):
    extensions += 'sphinxcontrib.spelling',
    spelling_show_suggestions = True
    spelling_lang = 'en_US'

source_suffix = '.rst'
master_doc = 'index'
project = 'rng2doc'
year = '2017'
author = 'Thomas Schraitle'
copyright = '{0}, {1}'.format(year, author)
version = release = '0.3.0'

autosummary_generate = True

pygments_style = 'trac'
templates_path = [ '_templates' ]
extlinks = {
    'bb': ('https://bitbucket.org/tomschr/rng2doc', None),
    'issue': ('https://bitbucket.org/tomschr/rng2doc/issues/%s', '#'),
    'pr': ('https://bitbucket.org/tomschr/rng2doc/pull-requests/%s', 'PR #'),
}
# on_rtd is whether we are on readthedocs.org
# on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

#if not on_rtd:  # only set the theme if we're building docs locally
#    html_theme = 'sphinx_rtd_theme'

html_theme = "bizstyle"
html_theme_options = {
    "rightsidebar": "false",
#    "relbarbgcolor": "black"
}

html_last_updated_fmt = '%b %d, %Y'
html_split_index = False
html_short_title = '%s-%s' % (project, version)

