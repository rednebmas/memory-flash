import unittest
from model.objects.note import Note
from model.card_generators.progression_generator import ProgressionGenerator

class TestProgressionGenerator(unittest.TestCase):
	def test_four_five_one_cards(self):
		cards = ProgressionGenerator.four_five_one_cards()
		# (12 unique notes + 5 enharmonics) * 3 inversions per chord = 51 total cards
		self.assertEqual(len(cards), 51)

	def test_four_five_one_from_one__root(self):
		# C E G, C F A, B D G
		chords = ProgressionGenerator.four_five_one_from_one(Note(name='C'), 2, 1, 0)

		# four (second inversion)
		root = chords[0]
		self.assertEqual(root.notes[0].name, 'C')
		self.assertEqual(root.notes[1].name, 'F')
		self.assertEqual(root.notes[2].name, 'A')

		# five (first inversion)
		root = chords[1]
		self.assertEqual(root.notes[0].name, 'B')
		self.assertEqual(root.notes[1].name, 'D')
		self.assertEqual(root.notes[2].name, 'G')

		# root (root inversion)
		root = chords[2]
		self.assertEqual(root.notes[0].name, 'C')
		self.assertEqual(root.notes[1].name, 'E')
		self.assertEqual(root.notes[2].name, 'G')

	def test_four_five_one_from_one__first_inversion(self):
		# C E G, C F A, B D G
		chords = ProgressionGenerator.four_five_one_from_one(Note(name='C'), 0, 2, 1)

		# four (root inversion)
		root = chords[0]
		self.assertEqual(root.notes[0].name, 'F')
		self.assertEqual(root.notes[1].name, 'A')
		self.assertEqual(root.notes[2].name, 'C')

		# five (second inversion)
		root = chords[1]
		self.assertEqual(root.notes[0].name, 'D')
		self.assertEqual(root.notes[1].name, 'G')
		self.assertEqual(root.notes[2].name, 'B')

		# root (first inversion)
		root = chords[2]
		self.assertEqual(root.notes[0].name, 'E')
		self.assertEqual(root.notes[1].name, 'G')
		self.assertEqual(root.notes[2].name, 'C')

	def test_four_five_one_from_one__second_inversion(self):
		# C E G, C F A, B D G
		chords = ProgressionGenerator.four_five_one_from_one(Note(name='C'), 1, 0, 2)

		# four (first inversion)
		root = chords[0]
		self.assertEqual(root.notes[0].name, 'A')
		self.assertEqual(root.notes[1].name, 'C')
		self.assertEqual(root.notes[2].name, 'F')

		# five (root inversion)
		root = chords[1]
		self.assertEqual(root.notes[0].name, 'G')
		self.assertEqual(root.notes[1].name, 'B')
		self.assertEqual(root.notes[2].name, 'D')

		# root (second inversion)
		root = chords[2]
		self.assertEqual(root.notes[0].name, 'G')
		self.assertEqual(root.notes[1].name, 'C')
		self.assertEqual(root.notes[2].name, 'E')


def main():
	unittest.main()

if __name__ == '__main__':
	main()