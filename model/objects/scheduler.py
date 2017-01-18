import random
from random import randint
from functools import reduce
from model.db import db
from model.objects.deck import Deck
from model.objects.card import Card
from model.objects.session import Session
from model.math_sam import choose_index_for_weights

class Scheduler:
	@staticmethod
	def next(session, not_card=None):
		if session.cards_loaded == False: session.load_cards()

		card = None
		session_stage = Scheduler.session_stage(session)
		if session_stage == "new cards":
			card = Deck.unseen_cards(session)[0]
		elif session_stage == "reviewing":
			card = Scheduler.weighted_random_card(session.cards, not_card)
			print('picked card: ' + str(card.answer_history.time_to_correct))
		elif session_stage == "finished":
			print('****************** started a new session *******************')

		return card, session_stage

	@staticmethod
	def weighted_random_card(cards, not_card):
		""" Cards is an array of cards where each card has an answer_history """
		weights = [card.answer_history.time_to_correct for card in cards]
		print('weights for random card')
		print(weights)
		learning_factor = 2.0
		index = choose_index_for_weights(weights, learning_factor)
		card = cards[index]

		if not_card is not None and card.card_id == not_card.card_id:
			return weighted_random_card(cards, not_card)
		else:
			return  card

	@staticmethod
	def session_stage(session):
		if session.cards_loaded == False: session.load_cards()
		cards_time_to_corrects = [card.answer_history.time_to_correct for card in session.cards]
		print()
		print('card_ids: ' + str([card.card_id for card in session.cards]))
		sum_time_to_correct = sum(cards_time_to_corrects)
		print('cards_time_to_corrects: ' + str(cards_time_to_corrects) + ', sum: ' + str(sum_time_to_correct) + ', session.median: ' + str(session.median))
		if sum_time_to_correct < 60.0 or len(session.cards) < 8 and len(Deck.unseen_cards(session)):
			print("new cards")
			return "new cards"
		elif len(cards_time_to_corrects) > 0 and session.median is not None and max(cards_time_to_corrects) < session.median:
			session.update_stage('finished')
			print("finished")
			return "finished"
		else:
			if session.stage == 'aquire':
				session.add_seen_cards()
				session.update_median()
				session.update_stage('speed up')
			print("reviewing")
			return "reviewing"
