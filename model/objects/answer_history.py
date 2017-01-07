from model.db import db

class AnswerHistory:
	@staticmethod
	def from_json(json):
		return AnswerHistory(
			json['session_id'], 
			json['card_id'], 
			json['time_to_correct'], 
			json['first_attempt_correct'], 
			json['answered_at'] if 'answered_at' in json else DB.datetime_now()
		) 

	def __init__(self, session_id, card_id, time_to_correct, first_attempt_correct, answered_at):
		self.session_id = session_id
		self.card_id = card_id
		self.time_to_correct = time_to_correct
		self.first_attempt_correct = first_attempt_correct
		self.answered_at = answered_at

	def __str__(self):
		return "Time to correct: {}".format(self.time_to_correct)

	def insert(self):
		#########   WARNING ##############
		conn = db.conn()
		cursor = conn.cursor()
		cursor.execute("""
			INSERT INTO AnswerHistory (session_id, card_id, time_to_correct, first_attempt_correct, answered_at)
			VALUES (?, ?, ?, ?, ?)
		 """, (self.session_id, 
		 	   self.card_id, 
		 	   self.time_to_correct, 
		 	   self.first_attempt_correct,
		 	   self.answered_at))

		# put into SessionCard if it doesn't already exist
		cursor.execute("SELECT COUNT(*) FROM SessionCard WHERE session_id = ? AND card_id = ?")
		count =  cursor.fetchone()[0] 
		if count == 0:
			cursor.execute("""
				INSERT INTO SessionCard (session_id, card_id)
				VALUES (?, ?, ?, ?, ?)
			 """, (self.session_id, 
			 	   self.card_id, 
			 	   self.time_to_correct, 
			 	   self.first_attempt_correct,
			 	   self.answered_at))

		db.commit()

