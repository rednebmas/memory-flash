import re
from model.objects.note import Note
from model.objects.interval import Interval

class Chord:
	"""
	self.intervals will always be relative to root position chord
	"""
	def __init__(self, name):
		self.name = name
		root_name, quality = re.search(r'([A-G][b#]?)(.*)', name).groups()
		self.root = Note(root_name)
		self.intervals = Chord.intervals_for_quality(quality) 
		self.notes = [self.root] + [self.root.transposed(interval) for interval in self.intervals]

	def inversion(self, num):
		""" num is an integer """
		def rotate(l, n): # http://stackoverflow.com/a/9457864/337934
			return l[n:] + l[:n]
		inverted = Chord(self.name)
		inverted.notes = rotate(inverted.notes, num)
		inverted.name = inverted.name + '/' + inverted.notes[0].name
		return inverted

	@staticmethod
	def intervals_for_quality(quality):
		if len(quality) == 0:
			return Chord.major_intervals()
		if len(quality) == 1:
			if quality[0] == "m":
				return Chord.minor_intervals()
			else:
				return []
		else:
			return []

	@staticmethod
	def major_intervals():
		return [Interval.M3(), Interval.P5()]

	@staticmethod
	def minor_intervals():
		return [Interval.m3(), Interval.P5()]