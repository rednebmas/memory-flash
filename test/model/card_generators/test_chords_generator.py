import unittest
from model.card_generators.chords_generator import ChordsGenerator

class TestChordGenerator(unittest.TestCase):
	def test_major_chord_generation(self):
		cards = ChordsGenerator.generate_major_chord_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertTrue(len(cards) == 51)

	def test_minor_chord_generation(self):
		cards = ChordsGenerator.generate_minor_chord_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertTrue(len(cards) == 51)

def main():
	unittest.main()

if __name__ == '__main__':
	main()