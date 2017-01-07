class Card:
	question = None
	question = None
	answer = None

	@staticmethod
	def from_db(row):
		return Card(row[0], row[1], row[2], row[3])

	def __init__(self, card_id, deck_id, question, answer):
		self.card_id = card_id
		self.deck_id = deck_id
		self.question = question
		self.answer = answer

	def as_dict(self):
		return {
			"card_id" : self.card_id,
			"deck_id" : self.deck_id,
			"question" : self.question,
			"answer" : self.answer
		}

	def set_answer_history(self, answer_history):
		self.answer_history = answer_history

