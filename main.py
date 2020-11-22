import sanic.config
sanic.config.Config.LOGO = ""
from sanic import Sanic
from sanic.response import json, html, text
from sanic_session import InMemorySessionInterface
from model.db import db
from model.objects.card import Card
from model.objects.deck import Deck
from model.objects.answer_history import AnswerHistory
from model.objects.session import Session
from model.objects.input_modality import InputModality
from viewmodel.deck_view_model import DeckViewModel
from viewmodel.card_view_model import CardViewModel
from routes.core import jinja_render, jinja_response
import os
import sys

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
app.static('/robots.txt', './view/public/robots.txt')
app.static('/.well-known', './.well-known') # certbot

paths_that_dont_need_auth = ['/decks', '/user/login', '/user', '/', '/user/create_account']

######################
# Session Middleware #
######################

@app.middleware('request')
async def add_session_to_request(request):
	print('###### request.args = ' + str(request.args))
	# before each request initialize a session
	# using the client's request
	await session_interface.open(request)
	# make sure user is authenticated to view most pages, otherwise, redirect to login
	if 'user_id' not in request.ctx.session and hasattr(request, 'path') and request.path not in paths_that_dont_need_auth:
		print('<' + request.path + '> Attempted to access route which requires you to be logged in to an account.')

		query_string = '?' 
		for key, val in request.query_args:
			if key == 'original_path': continue
			query_string += key + "=" + str(val)
		
		return sanic.response.redirect('/user/login?original_path=' + request.path + query_string)

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
	return jinja_response('decks.html', decks=decks)

@app.route("/")
async def index(request):
    return sanic.response.redirect('/decks')

@app.route("/decks/<deck_id:int>/cards")
async def decks_cards(request, deck_id):
	cards = list(CardViewModel.all_cards_from_deck(deck_id))
	return jinja_response('deck_cards.html', cards=cards)

@app.route("/decks/<deck_id:int>/study")
async def decks_study(request, deck_id):
	input_modality_id = request.args.get('input_modality_id', None)
	if input_modality_id is None:
		input_modalities = Deck.from_id(deck_id).input_modalities()
		return jinja_response('choose_input_modality.html', deck_id=deck_id, input_modalities=input_modalities)

	input_modality = InputModality.from_id(input_modality_id)
	deck = Deck.from_id(deck_id)

	# SOMEDAY: ensure that we have a valid input_modality_id for this deck
	user_id = request.ctx.session['user_id']
	session = Session.find_or_create(deck_id, user_id, input_modality_id)
	return jinja_response('study.html', deck=deck, mf_session=session, input_modality=input_modality, session=request.ctx.session)

@app.route("/session/<session_id:int>/next_card")
async def session_next_card(request, session_id):
	previous_card_ids = request.args.getlist('previous_card_ids[]', [])
	previous_card_ids = list( map(lambda c: int(c), previous_card_ids) )

	session = Session.from_db_id(session_id)
	card = session.next_card(previous_card_ids)

	if card is None:
		return json({ 'msg': 'session complete' })

	card.question = jinja_render(card.template_path, **card.template_data)
	res = card.as_dict()
	if session.median is not None:
		res['session'] = {}
		res['session']['median'] = session.median
		res['session']['total_cards'] = len(session.cards)
		res['session']['cards_below_median'] = len(session.cards_below_median())

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

import routes.user_routes
routes.user_routes.add_routes(app)

cert = '/etc/letsencrypt/live/mflash.sambender.com/cert.pem'
privkey = '/etc/letsencrypt/live/mflash.sambender.com/privkey.pem'

if 'release' in sys.argv:
	import ssl
	context = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)
	context.load_cert_chain(cert, keyfile=privkey)

	if __name__ == '__main__':
		redirect_to_http_to_https_app = Sanic("redirect_to_https")
		@redirect_to_http_to_https_app.middleware('request')
		async def redirect_to_https(request):
			return sanic.response.redirect('https://' + request.headers['host'])

		app_server = app.create_server(host="0.0.0.0", port=443, debug=False, ssl=context)
		redirect_server = redirect_to_http_to_https_app.create_server(host="0.0.0.0", port=80, debug=False)

		from signal import signal, SIGINT
		import asyncio
		import uvloop
		asyncio.set_event_loop(uvloop.new_event_loop())
		loop = asyncio.get_event_loop()
		task = asyncio.ensure_future(app_server)
		task = asyncio.ensure_future(redirect_server)
		signal(SIGINT, lambda s, f: loop.stop())
		try:
			loop.run_forever()
		except:
			loop.stop()
else:
	if __name__ == '__main__':
		app.run(host="0.0.0.0", port=8000, debug=True)
