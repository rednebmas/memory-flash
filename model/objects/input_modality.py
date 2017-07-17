from model.db import db

class InputModality:
	@staticmethod
	def from_id(input_modality_id):
		row = db.select1(
			table="InputModality", 
			where="input_modality_id = ?", 
			substitutions=(input_modality_id,)
		)
		return InputModality.from_db(row)

	@staticmethod
	def from_db(row):
		return InputModality(row['input_modality_id'], row['input_modality_name'])

	def __init__(self, input_modality_id, input_modality_name):
		self.input_modality_id = input_modality_id
		self.name = input_modality_name