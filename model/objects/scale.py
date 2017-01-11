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
