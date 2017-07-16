import unittest
from model.objects.deck import Deck
from model.objects.card import Card
from model.objects.session import Session
from model.objects.answer_history import AnswerHistory
from model.objects.input_modality import InputModality
from model.db import db, DB

class TestDeck(unittest.TestCase):

	def setUp(self):
		db.unittest_reset()

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

	def test_unseen_cards_same_deck_different_input_modality(self):
		user_id = 1
		deck_id = 3
		input_modality_id1 = 1

		session = Session.find_or_create(deck_id, user_id, input_modality_id1)
		session.load_cards()
		cards = Deck.unseen_cards(session)
		original_len_unseen_input_modality1 = len(cards)

		# mark one card as seen
		AnswerHistory(session.session_id, cards[0].card_id, user_id, 10.0, True, DB.datetime_now()).insert()

		# second session
		input_modality_id2 = 2
		session = Session.find_or_create(deck_id, user_id, input_modality_id2)
		session.load_cards()
		cards = Deck.unseen_cards(session)
		len_unseen_input_modality2 = len(cards)

		self.assertEqual(original_len_unseen_input_modality1, len_unseen_input_modality2)

	
	def test_input_modalities(self):
		input_modalities = Deck.from_id(1).input_modalities()
		self.assertEqual(len(input_modalities), 3)
		self.assertTrue(isinstance(input_modalities[0], InputModality))

def main():
	unittest.main()

if __name__ == '__main__':
	main()