import unittest
from model.db import db, DB
from model.migration_manager import MigrationManager
from model.objects.answer_history import AnswerHistory
from model.objects.scheduler import Scheduler
from model.objects.card import Card
from model.objects.session import Session
from model.objects.deck import Deck
from datetime import datetime, timedelta

deck_id = 3
input_modality_id = 1

class TestScheduler(unittest.TestCase):
	def setUp(self):
		db.unittest_reset()

	def test_behavior_test_part_2_and_seen_cards(self):
		user_id = 1
		self.test_behavior_test_part_1_new_cards()
		session = Session.new(deck_id, user_id, input_modality_id)

		deck = Deck.from_deck_id(session.deck_id)
		self.assertNotEqual(session.session_id, 1)
		self.assertEqual(session.stage, 'aquire')
		session.load_cards()
		self.assertEqual(len(session.cards), 0)

		### 
		# Get new cards
		### 

		new_cards = []

		two_seconds_ago = datetime.now() - timedelta(seconds=2)
		two_seconds_ago = two_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')

		for i in range(8):
			self.assertEqual(i, len(session.cards))
			self.assertEqual(Scheduler.session_stage(session), 'new cards')
			card, session_stage = Scheduler.next(session)

			new_cards.append(card)
			AnswerHistory(session.session_id, card.card_id, user_id, (float(i) + 1.0) * 10, True, two_seconds_ago).insert()
			session.load_cards()

		self.assertEqual(Scheduler.session_stage(session), 'reviewing')
		self.assertEqual(session.stage, 'speed up')
		session.load_cards()
		self.assertEqual(len(session.cards), int(8 * (1/3) + 8))

		###
		# Now test if moves to finished correctly
		###

		time_to_correct_list = sorted([card.answer_history.time_to_correct for card in session.cards])
		median = time_to_correct_list[int(len(session.cards) / 2)]
		self.assertEqual(session.median, median)

		###################################################################################################
		## 
		###################################################################################################

		previous_card = None
		loop_count = 0
		self.assertEqual(session.stage, 'speed up')
		while Scheduler.session_stage(session) == 'reviewing':
			self.assertTrue(loop_count < 100)
			loop_count += 1

			session.load_cards()
			card, session_stage = Scheduler.next(session, previous_card)
			if session_stage is not 'finished': 
				self.assertNotEqual(card, previous_card)
				AnswerHistory(session.session_id, card.card_id, user_id, median / 2.0, True, DB.datetime_now()).insert()
			else:
				break

		session.load_cards()
		self.assertEqual(Scheduler.session_stage(session), 'finished')

	def test_behavior_test_part_1_new_cards(self):
		user_id = 1
		session = Session.find_or_create(deck_id, user_id, input_modality_id)
		session.load_cards()
		self.assertEqual(len(session.cards), 0)

		### 
		# Get new cards
		### 
		new_cards = []
		two_seconds_ago = datetime.now() - timedelta(seconds=2)
		two_seconds_ago = two_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')

		for i in range(8):
			self.assertEqual(i, len(session.cards))
			self.assertEqual(Scheduler.session_stage(session), 'new cards')
			card, session_stage = Scheduler.next(session)

			new_cards.append(card)
			AnswerHistory(session.session_id, card.card_id, user_id, (float(i) + 1.0) * 10, True, two_seconds_ago).insert()
			session.load_cards()

		self.assertEqual(Scheduler.session_stage(session), 'reviewing')
		self.assertEqual(session.stage, 'speed up')
		self.assertTrue(len(session.cards) == 8) 
		self.assertTrue(session.median is not None)

		###
		# Now test if moves to finished correctly
		###

		time_to_correct_list = sorted([card.answer_history.time_to_correct for card in session.cards])
		median = time_to_correct_list[int(len(session.cards) / 2)]

		for new_card in new_cards:
			session.load_cards()
			self.assertEqual(Scheduler.session_stage(session), 'reviewing')
			AnswerHistory(session.session_id, new_card.card_id, user_id, median / 2.0, True, DB.datetime_now()).insert()

		session.load_cards()
		self.assertEqual(Scheduler.session_stage(session), 'finished')

def main():
	unittest.main()

if __name__ == '__main__':
	main()