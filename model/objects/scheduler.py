import random
from random import randint
from functools import reduce
from model.db import db
from model.objects.deck import Deck
from model.objects.card import Card
from model.objects.session import Session

class Scheduler:
	@staticmethod
	def next(session, not_card=None):
		if session.cards_loaded == False: session.load_cards()

		card = None
		session_stage = Scheduler.session_stage(session)
		if session_stage == "new cards":
			card = Scheduler.card_not_in_session(session)
		elif session_stage == "reviewing":
			if session.is_fully_initialized() == False: session.fully_initialize()
			card = Scheduler.weighted_random_card(session.cards, not_card)
			print('picked card: ' + str(card.answer_history.time_to_correct))
		elif session_stage == "finished":
			print('****************** started a new session *******************')
			session = Session.new_for_deck_id(session.deck_id)
			print(session)
			card, session = Scheduler.next(session)

		return card, session

	@staticmethod
	def card_not_in_session(session):
		deck = Deck.from_deck_id(session.deck_id)
		deck.load_cards()
		card = None
		while card is None:
			rand_index = randint(0, len(deck.cards) - 1) 
			card = deck.cards[rand_index]
			for c in session.cards:
				if c.card_id == card.card_id:
					card = None
					break
		return card

	@staticmethod
	def weighted_random_card(cards, not_card):
		""" Cards is an array of cards where each card has an answer_history """
		all_time_to_correct = [card.answer_history.time_to_correct for card in cards]
		learning_factor = 2.0
		learned_sum = reduce(lambda x, y: x+y**learning_factor, all_time_to_correct, 0)
		running_sum = 0.0
		rand_pos = random.random() * learned_sum
		print('learned sum = ' + str(learned_sum))
		print('rand pos = ' + str(rand_pos))
		for i in range(len(all_time_to_correct)):
			running_sum += all_time_to_correct[i]**learning_factor
			if rand_pos <= running_sum:
				card = cards[i]
				break

		if not_card is not None and card.card_id == not_card.card_id:
			return weighted_random_card(cards, not_card)
		else:
			return  card

	@staticmethod
	def session_stage(session):
		all_time_to_correct = [card.answer_history.time_to_correct for card in session.cards]
		print(all_time_to_correct)
		sum_time_to_correct = sum(all_time_to_correct)
		if sum_time_to_correct > 60 and len(session.cards):
			print("reviewing")
			return "reviewing"
		elif len(all_time_to_correct) > 0 and session.median is not None and max(all_time_to_correct) < session.median:
			print("finished")
			return "finished"
		else:
			print("new cards")
			return "new cards"
