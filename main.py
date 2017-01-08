from sanic import Sanic
from sanic.response import json, html, text
from jinja2 import Environment, FileSystemLoader
from model.db import db
from viewmodel.deck_view_model import DeckViewModel
from viewmodel.card_view_model import CardViewModel
from viewmodel.study_view_model import StudyViewModel
import os

app = Sanic(__name__)
app.static('/style', './view/css')
app.static('/img', './view/img')
app.static('/js', './view/js')
templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view'))

##########
# Routes #
##########

@app.route("/decks")
async def decks(request):
	decks = list(DeckViewModel.all_decks())
	return html(templates.get_template('decks.html').render(decks=decks))

@app.route("/decks/<deck_id:int>/cards")
async def decks_cards(request, deck_id):
	cards = list(CardViewModel.all_cards_from_deck(deck_id))
	return html(templates.get_template('deck_cards.html').render(cards=cards))

@app.route("/decks/<deck_id:int>/study")
async def decks_study(request, deck_id):
	deck, session = StudyViewModel.deck_and_session(deck_id)
	return html(templates.get_template('study.html').render(deck=deck, session=session))

@app.route("/session/<session_id:int>/next_card")
async def session_next_card(request, session_id):
	card = StudyViewModel.next_card(session_id, request.json['deck_id'])
	return json(card.as_dict())

@app.route("/")
async def index(request):
    return json({'hello':'memory-flash-2'})

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000, debug=True)
