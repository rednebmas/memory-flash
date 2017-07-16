import unittest
from model.objects.input_modality import InputModality
from model.db import db, DB

class TestInputModality(unittest.TestCase):
	def test_fa_icon_class(self):
		row = db.select1(table="InputModality", where="input_modality_id = ?", substitutions=(1,))
		input_modality = InputModality.from_db(row)
		self.assertTrue(input_modality.name, 'Text')

def main():
	unittest.main()

if __name__ == '__main__':
	main()