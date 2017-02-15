import os
from sanic.response import json, html, text
from jinja2 import Environment, FileSystemLoader
from sanic.views import HTTPMethodView

template_envirnoment = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))
template = template_envirnoment.get_template
