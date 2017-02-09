import unittest
from model.objects.scale import Scale
from model.objects.accidental import Accidental
from model.objects.note import Note

class TestScale(unittest.TestCase):
	def test_accidental_c(self):
		scale = Scale('C')
		self.assertTrue(scale.accidental == Accidental.sharp, scale.accidental)

	def test_accidental_f(self):
		scale = Scale('F')
		self.assertTrue(scale.accidental == Accidental.flat)

	def test_accidental_c_minor(self):
		scale = Scale('C minor')
		self.assertTrue(scale.accidental == Accidental.flat, scale.accidental)

	def test_major_scale_accidental_converter_c(self):
		self.assertTrue(Scale.major_scale_accidental_converter('C') == Accidental.sharp)

	def test_major_scale_accidental_converter_g(self):
		self.assertTrue(Scale.major_scale_accidental_converter('G') == Accidental.sharp)

	def test_major_type_automatic(self):
		scale = Scale('C')
		self.assertTrue(scale.type == 'major')

	def test_minor_type_parsed(self):
		scale = Scale('C minor')
		self.assertTrue(scale.type == 'minor')

	def test_root_with_minor_scale(self):
		scale = Scale('C minor')
		self.assertTrue(scale.root == Note('C'))

	def test_root_with_flat(self):
		scale = Scale('Bb')
		self.assertTrue(scale.root == Note('Bb'), scale.root)

	def test_degree_gb(self):
		scale = Scale('Gb')
		self.assertEqual(scale.degree(1).name, 'Gb') 
		self.assertEqual(scale.degree(2).name, 'Ab') 
		self.assertEqual(scale.degree(3).name, 'Bb') 
		self.assertEqual(scale.degree(4).name, 'Cb') 
		self.assertEqual(scale.degree(5).name, 'Db') 
		self.assertEqual(scale.degree(6).name, 'Eb') 
		self.assertEqual(scale.degree(7).name, 'F')

	def test_degree_f(self):
		scale = Scale('F')
		self.assertEqual(scale.degree(1).name, 'F') 
		self.assertEqual(scale.degree(2).name, 'G') 
		self.assertEqual(scale.degree(3).name, 'A') 
		self.assertEqual(scale.degree(4).name, 'Bb') 
		self.assertEqual(scale.degree(5).name, 'C') 
		self.assertEqual(scale.degree(6).name, 'D') 
		self.assertEqual(scale.degree(7).name, 'E')

	def test_degree_c(self):
		scale = Scale('C')
		self.assertEqual(scale.degree(1).name, 'C') 
		self.assertEqual(scale.degree(2).name, 'D') 
		self.assertEqual(scale.degree(3).name, 'E') 
		self.assertEqual(scale.degree(4).name, 'F') 
		self.assertEqual(scale.degree(5).name, 'G') 
		self.assertEqual(scale.degree(6).name, 'A') 
		self.assertEqual(scale.degree(7).name, 'B')

	def test_degree_csharp(self):
		scale = Scale('C#')
		self.assertEqual(scale.degree(1).name, 'C#') 
		self.assertEqual(scale.degree(2).name, 'D#') 
		self.assertEqual(scale.degree(3).name, 'E#') 
		self.assertEqual(scale.degree(4).name, 'F#') 
		self.assertEqual(scale.degree(5).name, 'G#') 
		self.assertEqual(scale.degree(6).name, 'A#') 
		self.assertEqual(scale.degree(7).name, 'B#')



def main():
	unittest.main()

if __name__ == '__main__':
	main()