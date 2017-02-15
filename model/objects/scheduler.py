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
	def next(session, previous_card_id=None):
		if session.cards_loaded == False: session.load_cards()

		card = None
		session_stage = Scheduler.session_stage(session)
		if session_stage == "new cards":
			cards = Deck.unseen_cards(session)
			card = cards[randint(0, min(len(cards) - 1, 11))]
		elif session_stage == "reviewing":
			card = Scheduler.weighted_random_card(session.cards, previous_card_id)
			print('picked card ttc: ' + str(card.answer_history.time_to_correct) + ", id: " + str(card.card_id))
		elif session_stage == "finished":
			print('****************** started a new session *******************')

		return card, session_stage

	@staticmethod
	def weighted_random_card(cards, previous_card_id):
		""" Cards is an array of cards where each card has an answer_history """
		weights = [card.answer_history.time_to_correct for card in cards]
		learning_factor = 2.0
		index = choose_index_for_weights(weights, learning_factor)
		card = cards[index]

		if previous_card_id is not None and card.card_id == previous_card_id:
			return Scheduler.weighted_random_card(cards, previous_card_id)
		else:
			return  card

	@staticmethod
	def session_stage(session):
		if session.cards_loaded == False: session.load_cards()
		cards_time_to_corrects = [card.answer_history.time_to_correct for card in session.cards]
		print()
		print('card_ids: ' + str([card.card_id for card in session.cards]))
		sum_time_to_correct = sum(cards_time_to_corrects)
		print('cards_time_to_corrects = ' + str(sorted(cards_time_to_corrects)) + '\nsum = ' + str(sum_time_to_correct) + '\nsession.median = ' + str(session.median))

		if session.stage == 'finished':
			print('finished')
			return 'finished'
		if ((sum_time_to_correct < 60.0 or len(session.cards) < 8) 
				and len(Deck.unseen_cards(session)) 
				and session.stage == 'aquire'):
			print("new cards")
			return "new cards"
		elif (len(cards_time_to_corrects) > 0 
				and session.median is not None 
				and max(cards_time_to_corrects) < session.median 
				and session.stage == 'speed up'):
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
