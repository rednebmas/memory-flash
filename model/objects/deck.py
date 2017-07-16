from model.db import db
from model.objects.card import Card
from model.objects.input_modality import InputModality

class Deck:
	@staticmethod
	def from_id(deck_id):
		return Deck.from_db(db.select1(table="Deck", where="deck_id = {}".format(deck_id)))

	@staticmethod
	def from_db(row):
		return Deck(row['deck_id'], row['name'], row['descr'])

	def __init__(self, deck_id, name, descr):
		self.deck_id = deck_id
		self.name = name
		self.descr = descr

	def load_cards(self):
		rows = db.select(table="Card", where="deck_id = ?", substitutions=(self.deck_id,))
		self.cards = list(map(lambda c: Card.from_db(c), rows))

	def input_modalities(self):
		sql = """
		SELECT IM.input_modality_id, IM.input_modality_name
		FROM InputModality IM
		JOIN DeckInputModality DIM ON DIM.input_modality_id = IM.input_modality_id
		WHERE DIM.deck_id = ?
		ORDER BY IM.input_modality_id
		"""
		db.execute(sql, (self.deck_id,))
		rows = db.cursor.fetchall()
		return list(map(lambda r: InputModality.from_db(r), rows))

	@staticmethod
	def unseen_cards(session):
		sql = """
		SELECT C.*
		FROM Card C
		LEFT JOIN 
			( 
				SELECT AH.card_id, AH.answer_history_id
				FROM AnswerHistory AH
				JOIN Session S on S.session_id = AH.session_id
				WHERE S.deck_id = ? AND S.input_modality_id  = ? AND S.user_id = ?
			) as XYZ ON C.card_id = XYZ.card_id
		WHERE C.deck_id = ?
			AND XYZ.answer_history_id IS NULL
		GROUP BY C.card_id
		ORDER BY C.card_id;
		"""
		db.execute(
			sql, 
			(
				session.deck_id, 
				session.input_modality_id, 
				session.user_id,
				session.deck_id
			)
		)
		rows = db.cursor.fetchall()
		return list(map(lambda r: Card.from_db(r), rows))
