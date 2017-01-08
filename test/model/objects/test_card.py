import unittest
from model.objects.card import Card
from model.db import db, DB

class TestCard(unittest.TestCase):
	def test_from_db_id(self):
		c = Card.from_db_id(1)
		self.assertTrue(c.card_id == 1)

		c = Card.from_db_id(-1)
		self.assertTrue(c is None)

def main():
	unittest.main()

if __name__ == '__main__':
	main()