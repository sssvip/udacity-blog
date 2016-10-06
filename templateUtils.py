"""
This module is utils for template
"""
__version__ = '0.1'
__author__ = 'David West'
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'html')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))


# through the templte file name to get html template in the folder 'html'
def get_html_template(name):
    return jinja_env.get_template(name)


# to render the variables in the template
def reder_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
