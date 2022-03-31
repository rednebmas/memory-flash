import re
from model.objects.note import Note
from model.objects.interval import Interval
from model.objects.scale import Scale
import mingus.core.chords as mingus_chords

class Chord:
	"""
	self.intervals will always be relative to root position chord
	"""
	def __init__(self, name):
		self.name = name
		root_name, self.quality = re.search(r'([A-G][b#]?)(.*)', name).groups()
		self.root = Note(root_name)
		self.intervals = Chord.intervals_for_quality(self.quality) 
		self.scale = Scale(self.root.name + ' minor') if 'm' in self.name else Scale(self.root.name)
		self.notes = [Note(note_name) for note_name in mingus_chords.from_shorthand(name)]
		self.inversion = 0

	def invert(self, num, bass_numeral=False):
		""" num is an integer """
		def rotate(l, n): # http://stackoverflow.com/a/9457864/337934
			return l[n:] + l[:n]
		inverted = Chord(self.name)
		inverted.notes = rotate(inverted.notes, num)
		if bass_numeral:
			inverted.name = inverted.name + '/' + ['','3','5','7'][num]
		else:
			inverted.name = inverted.name + '/' + inverted.notes[0].name
		inverted.inversion = num
		return inverted

	def quality_full(self):
		if len(self.quality) == 0:
			return "major"
		elif self.quality == 'maj7':
			return "major"
		elif self.quality == 'm7':
			return "minor"
		elif self.quality[0] == "m":
			return "minor"
		elif self.quality == "dim" or self.quality == "dim7":
			return "diminished"
		elif self.quality == "aug":
			return "augmented"
		elif self.quality == "7":
			return "mixolydian"
		elif self.quality == "m7b5":
			return "locrian"
		else:
			return "unknown quality"

	@property
	def pretty_name(self):
		return self.name.replace('##', '𝄪').replace('#', '♯').replace('b','♭').replace('dim', '°').replace('aug', '+')

	@staticmethod
	def intervals_for_quality(quality):
		if len(quality) == 0:
			return Chord.major_intervals()
		elif quality[0] == "m":
			return Chord.minor_intervals()
		elif quality == "dim":
			return Chord.diminished_intervals()
		else:
			return []

	@staticmethod
	def major_intervals():
		return [Interval.M3(), Interval.P5()]

	@staticmethod
	def minor_intervals():
		return [Interval.m3(), Interval.P5()]

	@staticmethod
	def diminished_intervals():
		return [Interval.m3(), Interval.TT()]

