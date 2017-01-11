import unittest
from model.objects.note import Note
from model.objects.interval import Interval
from model.objects.accidental import Accidental

class TestNotes(unittest.TestCase):

	#################### 
	## init_with_name ## 
	#################### 

	def test_init_with_name_c4(self):
		note = Note(name='C4')
		self.assertTrue(note.name == 'C')
		self.assertTrue(note.octave == 4)
		self.assertTrue(note.pretty_name == 'C')
		self.assertTrue(note.name_octave == 'C4')
		self.assertAlmostEqual(note.freq, 261.6255, places=3, msg="Freq = {}".format(note.freq))

	def test_init_with_name_bsharp2(self):
		note = Note(name='B#2')
		self.assertTrue(note.name == 'B#')
		self.assertTrue(note.octave == 2)
		self.assertTrue(note.name_octave == 'B#2')
		self.assertTrue(note.pretty_name == 'B♯')
		self.assertAlmostEqual(note.freq, 65.4064, places=3, msg="Freq = {}".format(note.freq))

	def test_init_with_name_fflat6(self):
		note = Note(name='fb6')
		self.assertTrue(note.name == 'Fb', msg=note.name)
		self.assertTrue(note.octave == 6)
		self.assertTrue(note.pretty_name == 'F♭')
		self.assertTrue(note.name_octave == 'Fb6')
		self.assertAlmostEqual(note.freq, 1318.51, places=3, msg="Freq = {}".format(note.freq))

	def test_init_with_name_gflat11(self):
		note = Note(name='gb11')
		self.assertTrue(note.name == 'Gb', msg=note.name)
		self.assertTrue(note.octave == 11)
		self.assertTrue(note.name_octave == 'Gb11')

	def test_octave_assigned_automatically(self):
		note = Note('C')
		self.assertTrue(note.name_octave == 'C4', note.name_octave)

	#################### 
	## init_with_freq ## 
	#################### 

	def test_init_with_freq_a4(self):
		note = Note(freq=440.0)
		self.assertTrue(note.name_octave == 'A4', msg="name_octave = {}".format(note.name_octave))

	def test_init_with_freq_fsharp5(self):
		note = Note(freq=739.99)
		self.assertTrue(note.pretty_name == 'F♯')
		self.assertTrue(note.name_octave == 'F#5', msg="name_octave = {}".format(note.name_octave))

	def test_init_with_freq_dsharp1(self):
		note = Note(freq=38.89)
		self.assertTrue(note.name_octave == 'D#1', msg="name_octave = {}".format(note.name_octave))

	def test_init_with_freq_eflat1(self):
		note = Note(freq=38.89, accidental=Accidental.flat)
		self.assertTrue(note.name_octave == 'Eb1', msg="name_octave = {}".format(note.name_octave))

	################ 
	## transposed ## 
	################ 

	def test_note_transposed_c4(self):
		note_c4 = Note(name="C4")
		note = note_c4.transposed(Interval(2))
		self.assertTrue(note.name_octave == "D4")

	def test_transposed_with_accidental_type(self):
		note_c4 = Note(name="C#")
		note = note_c4.transposed(Interval.M2(), accidental=Accidental.flat)
		self.assertTrue(note.name == "Eb", note.name)

	def test_transposed_from_flat_to_flat(self):
		from_note = Note(name="Eb")
		to_note = from_note.transposed(Interval.P5())
		self.assertTrue(to_note.name == 'Bb')

	################# 
	## enharmonics ## 
	#################

	def test_enharmonics(self):
		dsharp6 = Note(name="D#6")
		flat, sharp = dsharp6.enharmonics()
		self.assertTrue(flat.name_octave == 'Eb6')
		self.assertTrue(sharp.name_octave == 'D#6')

	########### 
	## other ## 
	########### 

	def test_isaltered(self):
		dsharp6 = Note(name="D#6")
		dflat6 = Note(name="Db6")
		c = Note(name="C4")
		self.assertTrue(dsharp6.isaltered())
		self.assertTrue(dflat6.isaltered())
		self.assertTrue(c.isaltered() == False)


	def test_half_steps_from_a4(self):
		self.assertTrue(Note.half_steps_from_a4('A', 4) == 0)

	def test_half_steps_away_from_a4_to_note_in_4th_octave(self):
		self.assertTrue(Note.half_steps_away_from_a4_to_note_in_4th_octave('A') == 0)

	def test_freq_from_name_octave_a4(self):
		freq = Note.freq_from_name_octave('A', 4)
		self.assertAlmostEqual(freq, 440.0)

	def test_freq_from_name_octave_a3(self):
		freq = Note.freq_from_name_octave('A', 3)
		self.assertAlmostEqual(freq, 220.0, msg="Freq = {}".format(freq))

	def test_freq_from_name_octave_c4(self):
		freq = Note.freq_from_name_octave('C', 4)
		self.assertAlmostEqual(freq, 261.6255, places=3, msg="Freq = {}".format(freq))

	def test_freq_from_name_octave_csharp2(self):
		freq = Note.freq_from_name_octave('C#', 2)
		self.assertAlmostEqual(freq, 69.2957, places=3, msg="Freq = {}".format(freq))

	def test_freq_from_name_octave_eflat6(self):
		freq = Note.freq_from_name_octave('Eb', 6)
		self.assertAlmostEqual(freq, 1244.51, places=1, msg="Freq = {}".format(freq))

	def test_half_steps_away_from_a4_to_note_in_4th_octave_handles_bsharp(self):
		octave_b_sharp = Note.half_steps_away_from_a4_to_note_in_4th_octave('B#') 
		octave_c = Note.half_steps_away_from_a4_to_note_in_4th_octave('C') 
		self.assertTrue(octave_b_sharp == octave_c)

	################
	## Accidental ##
	################

	def test_accidental(self):
		self.assertTrue(Note('C').accidental == Accidental.natural)
		self.assertTrue(Note('Bb').accidental == Accidental.flat)
		self.assertTrue(Note('G#').accidental == Accidental.sharp)

def main():
	unittest.main()

if __name__ == '__main__':
	main()