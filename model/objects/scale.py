from model.objects.interval import Interval
from model.objects.note import Note
from model.objects.accidental import Accidental

class Scale:
	def __init__(self, name):
		self.name = name
		self.root = Note(name=name.split(' ')[0])
		self.type = Scale.type_for_name(name)
		if self.type == 'minor':
			self.accidental = Scale.minor_scale_accidental_converter(self.root.name)
		else:
			self.accidental = Scale.major_scale_accidental_converter(self.root.name)

	def degree(self, num):
		names = ["C", "D" , "E" , "F" , "G" , "A" , "B"]
		expected_note = self.root.transposed(self.intervals[num-1])

		root_index = names.index(self.root.name[0])
		degree_index = (root_index + (num - 1)) % len(names)
		degree_note = Note(names[degree_index])
		expected_note_index = names.index(expected_note.name[0])

		if expected_note.name[0] == degree_note.name[0]:
			note = expected_note

		# For example...
		# root  = Gb, degree = 4
		# degree_note = C
		# expected_note = B
		# note should be Cb
		elif names[(degree_index - 1) % len(names)] == expected_note.name[0]: 
			note = Note(names[degree_index] + "b")
		else:
			note = Note(names[degree_index] + "#")
		return note
			
	@property
	def intervals(self):
		if self.type == 'major':
			return [
				Interval.P1(),
				Interval.M2(),
				Interval.M3(),
				Interval.P4(),
				Interval.P5(),
				Interval.M6(),
				Interval.M7(),
			]

	@staticmethod
	def type_for_name(name):
		split = name.split(' ')
		if len(split) == 1:
			return 'major'
		else:
			return split[1]

	@staticmethod
	def minor_scale_accidental_converter(note):
		return {
			"C" : Accidental.flat,
			"C#" : Accidental.sharp,
			"Db" : Accidental.flat,
			"D"  : Accidental.flat,
			"D#"  : Accidental.sharp,
			"Eb" : Accidental.flat,
			"E"  : Accidental.sharp,
			"F"  : Accidental.flat,
			"F#" : Accidental.sharp,
			"Gb" : Accidental.flat,
			"G"  : Accidental.flat,
			"G#"  : Accidental.sharp,
			"Ab" : Accidental.flat,
			"A"  : Accidental.sharp,
			"A#"  : Accidental.sharp,
			"Bb" : Accidental.flat,
			"B" : Accidental.sharp,
		}[note.name if isinstance(note, Note) else note]	

	@staticmethod
	def major_scale_accidental_converter(note):
		return {
			"Cb" : Accidental.flat,
			"C" : Accidental.sharp,
			"C#" : Accidental.sharp,
			"Db" : Accidental.flat,
			"D"  : Accidental.sharp,
			"D#"  : Accidental.sharp,
			"Eb" : Accidental.flat,
			"E"  : Accidental.sharp,
			"F"  : Accidental.flat,
			"F#" : Accidental.sharp,
			"Gb" : Accidental.flat,
			"G"  : Accidental.sharp,
			"G#"  : Accidental.sharp,
			"Ab" : Accidental.flat,
			"A"  : Accidental.sharp,
			"A#"  : Accidental.sharp,
			"Bb" : Accidental.flat,
			"B" : Accidental.sharp,
		}[note.name if isinstance(note, Note) else note]	
