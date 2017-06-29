import sanic.config
sanic.config.Config.LOGO = ""
from sanic import Sanic
from sanic.response import json, html, text
from sanic_session import InMemorySessionInterface
from model.db import db
from model.objects.card import Card
from model.objects.answer_history import AnswerHistory
from model.objects.session import Session
from viewmodel.deck_view_model import DeckViewModel
from viewmodel.card_view_model import CardViewModel
from viewmodel.study_view_model import StudyViewModel
from routes.core import jinja_render, jinja_response
import os

app = Sanic(__name__)
session_interface = InMemorySessionInterface()

from aoiklivereload import LiveReloader
reloader = LiveReloader()
reloader.start_watcher_thread()

app.static('/style', './view/css')
app.static('/img', './view/img')
app.static('/js', './view/js')
app.static('/sounds', './view/sounds')
app.static('/favicon.ico', './view/img/favicon.png')
app.static('/metronome', './view/html/metronome')

paths_that_dont_need_auth = ['/decks', '/user/login', '/user']

######################
# Session Middleware #
######################

@app.middleware('request')
async def add_session_to_request(request):
	# before each request initialize a session
	# using the client's request
	await session_interface.open(request)
	# make sure user is authenticated to view most pages, otherwise, redirect to login
	if 'user_id' not in request['session'] and request.path not in paths_that_dont_need_auth:
		print('<' + request.path + '> Attempted to access route which requires you to be logged in to an account.')
		return sanic.response.redirect('/user/login')

@app.middleware('response')
async def save_session(request, response):
	# after each request save the session,
	# pass the response to set client cookies
	await session_interface.save(request, response)

##########
# Routes #
##########

@app.route("/decks")
async def decks(request):
	decks = list(DeckViewModel.all_decks())
	print(request['session'])
	# print(request['session']['user_id'])
	return jinja_response('decks.html', decks=decks)

@app.route("/decks/<deck_id:int>/cards")
async def decks_cards(request, deck_id):
	cards = list(CardViewModel.all_cards_from_deck(deck_id))
	return jinja_response('deck_cards.html', cards=cards)

@app.route("/decks/<deck_id:int>/study")
async def decks_study(request, deck_id):
	deck, session = StudyViewModel.deck_and_session(request['session']['user_id'], deck_id)
	return jinja_response('study.html', deck=deck, session_id=session.session_id)

@app.route("/session/<session_id:int>/next_card")
async def session_next_card(request, session_id):
	card, session = StudyViewModel.next_card(
		request['session']['user_id'],
		session_id, 
		request.args.get('deck_id'),
		previous_card_id=request.args.get('previous_card_id', None)
	)
	if card is None:
		return json({ 'msg': 'session complete' })

	card.question = jinja_render(card.template_path, **card.template_data)
	res = card.as_dict()
	if session.median is not None:
		res['session_median'] = session.median

	return json(res)

@app.route("/session/<session_id:int>/complete")
async def session_complete(request, session_id):
	session = Session.from_db_id(session_id)
	return jinja_response('session_complete.html', deck_id=session.deck_id)

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
