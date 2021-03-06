import unittest
import model.db
import model.db
from model.db import DB, db
from model.objects.session import Session
from model.objects.card import Card
from model.objects.answer_history import AnswerHistory
from model.migration_manager import MigrationManager
import sqlite3

user_id = 1
input_modality_id = 1

class TestSession(unittest.TestCase):
	def setUp(self):
		db.unittest_reset()

	def test_find_or_create(self):
		sesh = Session.find_or_create(1, user_id, input_modality_id)
		self.assertTrue(sesh is not None)
		self.assertTrue(isinstance(sesh.session_id, int))

	def test_session_gets_correct_input_modality(self):
		sesh = Session.find_or_create(1, user_id, input_modality_id)
		self.assertTrue(sesh.input_modality_id == input_modality_id)

		sesh = Session.find_or_create(1, user_id, input_modality_id + 1)
		self.assertTrue(sesh.input_modality_id == input_modality_id + 1)

		sesh = Session.find_or_create(1, user_id, input_modality_id)
		self.assertTrue(sesh.input_modality_id == input_modality_id)

	def test_cards_is_initially_empty(self):
		session = Session.find_or_create(1, user_id, input_modality_id)
		session.load_cards()
		self.assertEqual(len(session.cards), 0)

		session = Session.find_or_create(2, user_id, input_modality_id)
		session.load_cards()
		self.assertEqual(len(session.cards), 0)

		session = Session.find_or_create(3, user_id, input_modality_id)
		session.load_cards()
		self.assertEqual(len(session.cards), 0)

	def test_from_db(self):
		session = Session.find_or_create(1, user_id, input_modality_id)
		row = db.select1(table="Session", where="deck_id = 1")
		session_from_db = Session.from_db(row)
		self.assertEqual(session_from_db.session_id, 1)
		self.assertEqual(session_from_db.deck_id, 1)
		self.assertTrue(session_from_db.begin_date is not None)
		self.assertEqual(session_from_db.stage, 'aquire')
		self.assertTrue(session_from_db.median is None)

	def test_update_stage(self):
		session = Session.find_or_create(1, user_id, input_modality_id)
		session.update_stage('speed up')
		row = db.select1(table="Session", where="session_id = ?", substitutions=(session.session_id,))
		self.assertEqual(row['stage'], 'speed up')

	def test_load_cards_loads_most_recent_answer_history(self):
		session = Session.find_or_create(1, user_id, input_modality_id)
		from datetime import datetime, timedelta
		two_seconds_ago = datetime.now() - timedelta(seconds=2)
		two_seconds_ago = two_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')

		card_id = db.select1(table="Card", where="deck_id = ?", substitutions=(session.deck_id,))['card_id']

		AnswerHistory(session.session_id, card_id, user_id, 1.12, True, two_seconds_ago).insert()
		session.load_cards()
		self.assertEqual(len(session.cards), 1)
		self.assertEqual(session.cards[0].answer_history.time_to_correct, 1.12)

		AnswerHistory(session.session_id, card_id, user_id, 2.12, True, DB.datetime_now()).insert()
		session.load_cards()
		self.assertEqual(len(session.cards), 1)
		self.assertEqual(session.cards[0].answer_history.time_to_correct, 2.12)

	def test_find_or_create_gives_new_session_if_stage_is_finished(self):
		session = Session.find_or_create(3, user_id, input_modality_id)
		session.update_stage('finished')
		session2 = Session.find_or_create(3, user_id, input_modality_id)
		self.assertNotEqual(session.session_id, session2.session_id)

	def test_next_card(self):
		sesh = Session.find_or_create(1, user_id, input_modality_id)
		card = sesh.next_card()
		self.assertTrue(isinstance(card, Card), card)


def main():
	unittest.main()

if __name__ == '__main__':
	main()