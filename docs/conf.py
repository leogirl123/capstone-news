project = 'News Application (Django Capstone)'
author = 'Jensi'
release = '1.0.0'

import os, sys, django
sys.path.insert(0, os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.py.settings')
django.setup()

extensions = ['sphinx.ext.autodoc','sphinx.ext.napoleon','sphinx.ext.viewcode']
html_theme = 'sphinx_rtd_theme'
napoleon_google_docstring = True
napoleon_numpy_docstring = True

templates_path = ['_templates']
exclude_patterns = []
html_static_path = ['_static']
