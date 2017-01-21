import unittest
from model.card_generators.notes_generator import NotesGenerator

class TestNotesGenerator(unittest.TestCase):
	def test_treble_cards(self):
		cards = NotesGenerator.treble_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertTrue(len(cards) > 0)

def main():
	unittest.main()

if __name__ == '__main__':
	main()