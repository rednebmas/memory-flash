from sanic import Sanic
from sanic.response import json, html, text
from jinja2 import Environment, FileSystemLoader
from model.db import db
from model.objects.card import Card
from model.objects.answer_history import AnswerHistory
from model.objects.session import Session
from viewmodel.deck_view_model import DeckViewModel
from viewmodel.card_view_model import CardViewModel
from viewmodel.study_view_model import StudyViewModel
import os

app = Sanic(__name__)
app.static('/style', './view/css')
app.static('/img', './view/img')
app.static('/js', './view/js')
app.static('/sounds', './view/sounds')
app.static('/favicon.ico', './view/img/favicon.png')
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
	if 'previous_card_id' not in request.args: request.args['previous_card_id'] = [None]
	card = StudyViewModel.next_card(session_id, request.args.get('deck_id'), previous_card_id=request.args.get('previous_card_id'))
	if card is None:
		return json({ 'msg': 'session complete' })
	card.question = templates.get_template(card.template_path).render(card.template_data)
	return json(card.as_dict())

@app.route("/session/<session_id:int>/complete")
async def session_complete(request, session_id):
	session = Session.from_db_id(session_id)
	return html(templates.get_template('session_complete.html').render(deck_id=session.deck_id))

@app.route("/card/<card_id:int>/answer", methods=['POST'])
async def answer_card(request, card_id):
	card = Card.from_db_id(card_id)
	if card is not None:
		AnswerHistory.from_json(request.json).insert()
		return json({ "success": True })
	return json({ "success": False })

@app.route("/")
async def index(request):
    return json({'hello':'memory-flash-2'})

import routes.user_routes
routes.user_routes.add_routes(app)

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=8000, debug=True)
