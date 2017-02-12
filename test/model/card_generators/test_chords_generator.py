import unittest
from model.card_generators.chords_generator import ChordsGenerator

class TestChordGenerator(unittest.TestCase):
	def test_major_chord_generation(self):
		cards = ChordsGenerator.generate_major_chord_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertTrue(len(cards) > 35)

	def test_minor_chord_generation(self):
		cards = ChordsGenerator.generate_minor_chord_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertTrue(len(cards) > 35)

	def test_dim_chord_generation(self):
		cards = ChordsGenerator.generate_dim_chords_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertTrue(len(cards) > 35)
		for card in cards:
			self.assertTrue('°' in card['question'])

def main():
	unittest.main()

if __name__ == '__main__':
	main()