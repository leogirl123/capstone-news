# -- Project information -----------------------------------------------------
project = 'News Application (Django Capstone)'
author = 'Jensi'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
import os, sys, django
sys.path.insert(0, os.path.abspath('..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')  # <-- your package
django.setup()

extensions = ['sphinx.ext.autodoc','sphinx.ext.napoleon','sphinx.ext.viewcode']
templates_path = ['_templates']
exclude_patterns = []
napoleon_google_docstring = True
napoleon_numpy_docstring = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
