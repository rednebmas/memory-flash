import json
from model.db import db

class Card:
	@staticmethod
	def from_db(row):
		return Card(row['card_id'], row['deck_id'], row['answer'], row['answer_validator'], row['accidental'], row['scale'], row['template_path'], json.loads(row['template_data']))

	@staticmethod
	def from_db_id(card_id):
		try:
			row = db.select1(table="Card", where="card_id = ?", substitutions=(card_id,))
			return Card.from_db(row)
		except Exception as e:
			return None

	def __init__(self, card_id, deck_id, answer, answer_validator, accidental, scale, template_path, template_data):
		self.card_id = card_id
		self.deck_id = deck_id
		self.answer = answer
		self.answer_validator = answer_validator
		self.accidental = accidental
		self.scale = scale
		self.template_path = template_path
		self.template_data = template_data
		self.answer_history = None

	def as_dict(self):
		result = {
			"card_id" : self.card_id,
			"deck_id" : self.deck_id,
			"question" : self.question if self.question is not None else "card does not have question",
			"answer" : self.answer,
			"answer_validator" : self.answer_validator,
			"accidental" : self.accidental,
			"scale" : self.scale,
			"template_path" : self.template_path,
			"template_data" : self.template_data,
		}

		if self.answer_history is not None and self.answer_history.time_to_correct is not None:
			result['prev_time_to_correct'] = self.answer_history.time_to_correct
			result['prev_first_attempt_correct'] = self.answer_history.first_attempt_correct
		
		return result

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


