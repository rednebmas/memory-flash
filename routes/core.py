import os
from sanic.response import json, html, text
from jinja2 import Environment, FileSystemLoader
from sanic.views import HTTPMethodView

template_envirnoment = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))
template = template_envirnoment.get_template

# using this method attaches the session to the template
def jinja_render(template_path, **kwargs):
	import inspect
	frame = inspect.currentframe()

	try:
		if inspect.getframeinfo(frame.f_back)[2] == 'jinja_response':
			session = frame.f_back.f_back.f_locals['request']['session']
		else:
			session = frame.f_back.f_locals['request']['session']

		return template(template_path).render(session=session, **kwargs)
	except Exception as e:
		return template(template_path).render(**kwargs)
	finally:
		# forgetting to delete the frame can cause reference cycles
		# https://docs.python.org/3/library/inspect.html#the-interpreter-stack
		del frame

def jinja_response(template_path, **kwargs):
	return html(jinja_render(template_path, **kwargs))
