from model.db import db
from model.objects.deck import Deck
from model.objects.session import Session
from model.objects.scheduler import Scheduler

class StudyViewModel:

	@staticmethod
	def deck_and_session(user_id, deck_id):
		deck = Deck.from_db(db.select1(table="Deck", where="deck_id = "+str(deck_id)))
		session = Session.from_deck_id(user_id, deck_id)
		return deck, session

	@staticmethod
	def next_card(user_id, session_id, deck_id, previous_card_id=None):
		if previous_card_id is not None: previous_card_id = int(previous_card_id)
		session = Session.from_deck_id(user_id, deck_id)
		card, state = Scheduler.next(session, previous_card_id)
		return card, session

