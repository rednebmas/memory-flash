from sanic import Sanic
from sanic.response import json, html
from jinja2 import Environment, FileSystemLoader
from model.db import db
import os

app = Sanic(__name__)
app.static('/style', './view/css')
app.static('/img', './view/img')
app.static('/js', './view/js')
templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view'))

@app.route("/decks")
async def decks(request):
	# decks = list(DeckViewModel.all_decks())
	return html(templates.get_template('decks.html').render(decks=decks))

@app.route("/")
async def index(request):
    return json({'hello':'asdf'})

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000, debug=True)
