import unittest
from model.objects.chord import Chord
from model.objects.note import Note
from model.objects.interval import Interval

class TestChord(unittest.TestCase):
	def test_c_major(self):
		c = Chord('C')

		self.assertTrue(c.name == 'C')
		self.assertTrue(c.root.name == 'C')
		self.assertTrue(len(c.intervals) == 2)
		self.assertTrue(c.intervals[0] == Interval.M3())
		self.assertTrue(c.intervals[1] == Interval.P5())

		self.assertTrue(len(c.notes) == 3)
		self.assertTrue(c.notes[0].name == 'C')
		self.assertTrue(c.notes[1].name == 'E')
		self.assertTrue(c.notes[2].name == 'G')

	def test_c_minor(self):
		c = Chord('Cm')

		self.assertTrue(c.name == 'Cm')
		self.assertTrue(c.root.name == 'C')
		self.assertTrue(len(c.intervals) == 2)
		self.assertTrue(c.intervals[0] == Interval.m3())
		self.assertTrue(c.intervals[1] == Interval.P5())

		self.assertTrue(len(c.notes) == 3)
		self.assertTrue(c.notes[0].name == 'C')
		self.assertTrue(c.notes[1].name == 'Eb')
		self.assertTrue(c.notes[2].name == 'G')

	def test_major_flat_chord(self):
		c = Chord('Bb')

		self.assertTrue(c.root.name == 'Bb')
		self.assertTrue(len(c.notes) == 3)
		self.assertTrue(c.notes[0].name == 'Bb')
		self.assertTrue(c.notes[1].name == 'D')
		self.assertTrue(c.notes[2].name == 'F')

	def test_first_inverted(self):
		c = Chord('C').invert(1)

		self.assertTrue(c.name == 'C/E')
		self.assertTrue(c.root.name == 'C')
		self.assertTrue(len(c.notes) == 3)
		self.assertTrue(c.notes[0].name == 'E')
		self.assertTrue(c.notes[1].name == 'G')
		self.assertTrue(c.notes[2].name == 'C')

	def test_second_inverted(self):
		c = Chord('Bb').invert(2)

		self.assertTrue(c.name == 'Bb/F')
		self.assertTrue(c.root.name == 'Bb')
		self.assertTrue(len(c.notes) == 3)
		self.assertTrue(c.notes[0].name == 'F')
		self.assertTrue(c.notes[1].name == 'Bb')
		self.assertTrue(c.notes[2].name == 'D')

	def test_pretty_name_major(self):
		c = Chord('Bb').invert(2)
		self.assertTrue(c.pretty_name == 'B♭/F')

	def test_diminished_chord(self):
		c = Chord('Cdim')
		self.assertTrue(c.root.name == 'C')
		self.assertTrue(len(c.notes) == 3)
		self.assertTrue(c.notes[0].name == 'C')
		self.assertTrue(c.notes[1].name == 'Eb')
		self.assertEqual(c.notes[2].name, 'Gb')
		self.assertEqual(c.pretty_name, 'C°')
		self.assertEqual(c.name, 'Cdim')

	def test_diminished_first_inversion(self):
		c = Chord('Cdim').invert(1)
		self.assertTrue(c.root.name == 'C')
		self.assertTrue(len(c.notes) == 3)
		self.assertEqual(c.notes[0].name, 'Eb')
		self.assertEqual(c.notes[1].name, 'Gb')
		self.assertEqual(c.notes[2].name, 'C')
		self.assertEqual(c.pretty_name, 'C°/E♭')
		self.assertEqual(c.name, 'Cdim/Eb')

	def test_diminished_second_inversion(self):
		c = Chord('Cdim').invert(2)
		self.assertTrue(c.root.name == 'C')
		self.assertTrue(len(c.notes) == 3)
		self.assertEqual(c.notes[0].name, 'Gb')
		self.assertEqual(c.notes[1].name, 'C')
		self.assertEqual(c.notes[2].name, 'Eb')
		self.assertEqual(c.pretty_name, 'C°/G♭')
		self.assertEqual(c.name, 'Cdim/Gb')

	def test_gsharp_major(self):
		c = Chord('G#')
		self.assertEqual(c.notes[0].name, 'G#')
		self.assertEqual(c.notes[1].name, 'B#')
		self.assertEqual(c.notes[2].name, 'D#')


def main():
	unittest.main()

if __name__ == '__main__':
	main()