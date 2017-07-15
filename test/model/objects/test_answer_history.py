import unittest
from model.objects.answer_history import AnswerHistory
from model.objects.session import Session
from model.db import db, DB

class TestAnswerHistory(unittest.TestCase):
	def test_insert(self):
		current_count = db.select(table="AnswerHistory", columns="COUNT(*)")[0]['COUNT(*)']
		ah_obj = AnswerHistory(1, 1, 1, 1.0, False, DB.datetime_now())
		ah_obj.insert()
		after_insert_count = db.select(table="AnswerHistory", columns="COUNT(*)")[0]['COUNT(*)']
		self.assertTrue(current_count + 1 == after_insert_count, after_insert_count)

	def test_first_review_from_last_day_reviewed_not_in_session(self):
		user_id = 1
		input_modality_id = 1
		deck_id = 1
		session = Session.find_or_create(deck_id, user_id, input_modality_id)

		from datetime import datetime, timedelta
		two_seconds_ago = datetime.now() - timedelta(seconds=2)
		two_seconds_ago = two_seconds_ago.strftime('%Y-%m-%d %H:%M:%S')

		card_id = db.select1(table="Card", where="deck_id = ?", substitutions=(session.deck_id,))['card_id']

		AnswerHistory(session.session_id + 10, card_id, user_id, 1.12, True, two_seconds_ago).insert()
		AnswerHistory(session.session_id + 10, card_id, user_id, 2.12, True, DB.datetime_now()).insert()
		answer_histories = AnswerHistory.first_review_from_last_day_reviewed_not_in_session(session)
		self.assertEqual(len(answer_histories), 1)
		self.assertEqual(answer_histories[0]['time_to_correct'], 1.12)
	
def main():
	unittest.main()

if __name__ == '__main__':
	main()