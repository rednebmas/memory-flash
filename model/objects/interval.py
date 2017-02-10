from model.objects.note import Note

class Interval:
	def __init__(self, quality, number):
		self.number = number
		self.quality, self.quality_long = Interval.short_long_quality_for_quality(quality)
		half_steps_modifier_for_quality = {
			"perfect" : 0,
			"major" : 0,
			"minor" : -1,
			"augmented" : 1
		}
		self.half_steps = Interval.major_scale_degree_to_half_steps()[number] + half_steps_modifier_for_quality[self.quality_long]

	def descending(self):
		interval = Interval(self.quality, self.number)
		interval.half_steps = interval.half_steps * -1
		return interval
		
	def name(self):
		return self.longdir() + " " + self.longname()

	def shortname(self):
		shortnames = {
			0  : "P1",
			1  : "m2",
			2  : "M2",
			3  : "m3",
			4  : "M3",
			5  : "P4",
			6  : "TT",
			7  : "P5",
			8  : "m6",
			9  : "M6",
			10 : "m7",
			11 : "M7",
			12 : "P8"
		}
		return shortnames[abs(self.half_steps)]

	def longname(self):
		longnames = {
			0  : "Unison",
			1  : "Minor Second",
			2  : "Major Second",
			3  : "Minor Third",
			4  : "Major Third",
			5  : "Perfect Fourth",
			6  : "Tritone",
			7  : "Perfect Fifth",
			8  : "Minor Sixth",
			9  : "Major Sixth",
			10 : "Minor Seventh",
			11 : "Major Seventh",
			12 : "Octave"
		}
		return longnames[abs(self.half_steps)]


	def shortdir(self):
		if self.half_steps == 0: return ""
		return "asc" if self.half_steps > 0 else "desc"

	def longdir(self):
		if self.half_steps == 0: return ""
		return "ascending" if self.half_steps > 0 else "descending"

	def __str__(self):
		return self.shortdir() + " " + self.shortname()

	def __eq__(self, other):
		"""Override the default Equals behavior"""
		if isinstance(other, self.__class__):
			return other.half_steps == self.half_steps
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	def __sub__(self, other):
		return Interval.from_half_steps(self.half_steps - other.half_steps, self.quality_long)

	@staticmethod
	def major_scale_degree_to_half_steps():
		return	{
			1 : 0, # p1
			2 : 2, # M2
			3 : 4, # M3
			4 : 5, # P4
			5 : 7, # P5
			6 : 9, # M6
			7 : 11, # M7
			8 : 12, # P8
		}

	@staticmethod
	def from_half_steps(half_steps, quality=None):
		half_steps_to_number = {
			0 : 1, # p1
			1 : 2, # m2
			2 : 2, # M2
			3 : 3, # m3
			4 : 3, # M3
			5 : 4, # P4
			6 : 4, # A4
			7 : 5, # P5
			8 : 6, # m6
			9 : 6, # M6
			10 : 7, # m7
			11 : 7, # M7
			12 : 8, # P8
		}
		if quality is None and half_steps in Interval.major_scale_degree_to_half_steps():
			quality = "major"
		elif quality is None:
			quality = "minor"
		return Interval(quality, half_steps_to_number[half_steps])

	@staticmethod
	def short_long_quality_for_quality(quality):
		short_to_long = {
			"M" : "major",
			"m" : "minor",
			"P" : "perfect",
			"A" : "augmented"
		}
		long_to_short = {v: k for k, v in short_to_long.items()}
		if len(quality) == 1:
			short_quality = quality
			long_quality = short_to_long[quality]
		else:
			short_quality = long_to_short[quality]
			long_quality = quality
		return short_quality, long_quality

	@staticmethod
	def between(note1, note2):
		return Interval.from_half_steps(note2.half_steps_from_a4 - note1.half_steps_from_a4)

	@staticmethod
	def P1():
		return Interval("perfect", 1)

	@staticmethod
	def m2():
		return Interval("minor", 2)

	@staticmethod
	def M2():
		return Interval("major", 2)

	@staticmethod
	def m3():
		return Interval("minor", 3)

	@staticmethod
	def M3():
		return Interval("major", 3)

	@staticmethod
	def P4():
		return Interval("perfect", 4)

	@staticmethod
	def TT():
		# https://en.wikipedia.org/wiki/Tritone#Augmented_fourth_and_diminished_fifth
		return Interval("augmented", 4)

	@staticmethod
	def P5():
		return Interval("perfect", 5)

	@staticmethod
	def m6():
		return Interval("minor", 6)

	@staticmethod
	def M6():
		return Interval("major", 6)

	@staticmethod
	def m7():
		return Interval("minor", 7)

	@staticmethod
	def M7():
		return Interval("major", 7)

	@staticmethod
	def P8():
		return Interval("perfect", 8)

	@staticmethod
	def all():
		return [
			Interval.M7().descending(),
			Interval.m7().descending(),
			Interval.M6().descending(),
			Interval.m6().descending(),
			Interval.P5().descending(),
			Interval.TT().descending(),
			Interval.P4().descending(),
			Interval.M3().descending(),
			Interval.m3().descending(),
			Interval.M2().descending(),
			Interval.m2().descending(),

			Interval.P1(),

			Interval.m2(),
			Interval.M2(),
			Interval.m3(),
			Interval.M3(),
			Interval.P4(),
			Interval.TT(),
			Interval.P5(),
			Interval.m6(),
			Interval.M6(),
			Interval.m7(),
			Interval.M7(),
		]

