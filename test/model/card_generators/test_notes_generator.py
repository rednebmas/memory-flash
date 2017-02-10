import unittest
from model.card_generators.notes_generator import NotesGenerator

class TestNotesGenerator(unittest.TestCase):
	def test_treble_cards(self):
		cards = NotesGenerator.treble_cards()
		self.assertTrue(len(cards) > 0)

def main():
	unittest.main()

if __name__ == '__main__':
	main()