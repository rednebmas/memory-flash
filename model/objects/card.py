from model.db import db

class Card:
	@staticmethod
	def from_db(row):
		return Card(row['card_id'], row['deck_id'], row['question'], row['answer'], row['answer_validator'], row['accidental'])

	@staticmethod
	def from_db_id(card_id):
		try:
			row = db.select1(table="Card", where="card_id = ?", substitutions=(card_id,))
			return Card.from_db(row)
		except Exception as e:
			return None

	def __init__(self, card_id, deck_id, question, answer, answer_validator, accidental):
		self.card_id = card_id
		self.deck_id = deck_id
		self.question = question
		self.answer = answer
		self.answer_validator = answer_validator
		self.accidental = accidental

	def as_dict(self):
		return {
			"card_id" : self.card_id,
			"deck_id" : self.deck_id,
			"question" : self.question,
			"answer" : self.answer,
			"answer_validator" : self.answer_validator,
			"accidental" : self.accidental
		}

	def set_answer_history(self, answer_history):
		self.answer_history = answer_history

	def __eq__(self, other):
		"""Override the default Equals behavior"""
		if isinstance(other, self.__class__):
			return other.card_id == self.card_id
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)


