from sanic import Sanic
from sanic.response import json, html, text
from jinja2 import Environment, FileSystemLoader
from model.db import db
from model.objects.card import Card
from model.objects.answer_history import AnswerHistory
from viewmodel.deck_view_model import DeckViewModel
from viewmodel.card_view_model import CardViewModel
from viewmodel.study_view_model import StudyViewModel
import os

app = Sanic(__name__)
app.static('/style', './view/css')
app.static('/img', './view/img')
app.static('/js', './view/js')
app.static('/sounds', './view/sounds')
templates = Environment(loader=FileSystemLoader(os.getcwd() + '/view/html'))

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
	if 'previous_card_id' not in request.json: request.json['previous_card_id'] = None
	card = StudyViewModel.next_card(session_id, request.json['deck_id'], previous_card_id=request.json['previous_card_id'])
	return json(card.as_dict())

@app.route("/card/<card_id:int>/answer")
async def answer_card(request, card_id):
	card = Card.from_db_id(card_id)
	if card is not None:
		AnswerHistory.from_json(request.json).insert()
		return json({ "success": True })
	return json({ "success": False })

@app.route("/")
async def index(request):
    return json({'hello':'memory-flash-2'})

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000, debug=True)
