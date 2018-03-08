# -*- coding: utf-8 -*-

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'testsettings'

extensions = [
  'sphinx.ext.todo',
  'sphinx.ext.ifconfig',
  'sphinx.ext.autodoc',
  ]
#templates_path = [os.path.join('..', 'templates')]
#html_theme_path = [os.path.join('..', 'themes')]
#html_static_path = [os.path.join('..', 'static')]
source_suffix = '.rst'
master_doc = 'index'
project = u'dream-usedb'
copyright = u'Haltu'
version = '1.0'
release = '1.0'
language = 'en'
html_title = project
unused_docs = []
exclude_trees = []
feed_base_url = 'http://localhost'
feed_description = project
pygments_style = 'colorful'
#html_theme = 'agogo'
html_theme = 'nature'
#html_theme = 'basic'
html_theme_options = {}
html_use_modindex = False
html_use_index = True
html_show_sourcelink = False
html_copy_source = False
html_file_suffix = '.html'
html_last_updated_fmt = '%b %d, %Y'
html_add_permalinks = False
#html_use_smartypants = True
html_additional_pages = {
#  'index': 'index.html',
  }

