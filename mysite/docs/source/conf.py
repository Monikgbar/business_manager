# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# Path setup
import os
import sys
import django


sys.path.insert(0, os.path.abspath('../..'))

# Django configuration
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

django.setup()


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Business Manager'
copyright = '2024, Mónica González Barreto'
author = 'Mónica González Barreto'
release = '0.1.0-alpha'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',    # Extension for autodoc
    'sphinx.ext.viewcode',   # Extension to view the source code
    'sphinx.ext.napoleon',   # Extension for Google/Numpy docstrings support
]

templates_path = ['_templates']
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
