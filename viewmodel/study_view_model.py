from model.db import db
from model.objects.deck import Deck
from model.objects.session import Session
from model.objects.scheduler import Scheduler

class StudyViewModel:

	@staticmethod
	def deck_and_session(deck_id):
		deck = Deck.from_db(db.select1(table="Deck", where="deck_id = "+str(deck_id)))
		session = Session.from_deck_id(deck_id)
		return deck, session

	@staticmethod
	def next_card(session_id, deck_id, not_card=None):
		session = Session.from_deck_id(deck_id)
		card, state = Scheduler.next(session, not_card)
		return card

