import unittest
from model.objects.deck import Deck
from model.objects.card import Card
from model.objects.session import Session
from model.objects.answer_history import AnswerHistory
from model.db import db, DB

class TestDeck(unittest.TestCase):
	def test_unseen_cards(self):
		user_id = 1
		deck_id = 3
		input_modality_id = 1

		session = Session.find_or_create(deck_id, user_id, input_modality_id)
		session.load_cards()

		cards = Deck.unseen_cards(session)
		card = cards[0]
		self.assertTrue(card is not None)
		self.assertTrue(isinstance(card, Card))

		AnswerHistory(session.session_id, card.card_id, user_id, 10.0, True, DB.datetime_now()).insert()
		cards = Deck.unseen_cards(session)
		self.assertNotEqual(card.template_data, cards[0].template_data)
		card = cards[0]

		cards = Deck.unseen_cards(session)
		self.assertEqual(card.template_data, cards[0].template_data)

def main():
	unittest.main()

if __name__ == '__main__':
	main()