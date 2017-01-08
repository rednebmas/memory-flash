import unittest
from model.objects.answer_history import AnswerHistory
from model.db import db, DB

class TestAnswerHistory(unittest.TestCase):
	def test_insert(self):
		current_count = db.select(table="AnswerHistory", columns="COUNT(*)")[0]['COUNT(*)']
		ah_obj = AnswerHistory(1, 1, 1.0, False, DB.datetime_now())
		ah_obj.insert()
		after_insert_count = db.select(table="AnswerHistory", columns="COUNT(*)")[0]['COUNT(*)']
		self.assertTrue(current_count + 1 == after_insert_count, after_insert_count)

def main():
	unittest.main()

if __name__ == '__main__':
	main()