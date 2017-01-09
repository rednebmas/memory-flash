class Interval:
	def __init__(self, half_steps):
		self.half_steps = half_steps

	def descending(self):
		return Interval(-self.half_steps)
		
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
		return "asc" if self.half_steps > 0 else "desc"

	def longdir(self):
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

	@staticmethod
	def P1():
		return Interval(0)

	@staticmethod
	def m2():
		return Interval(1)

	@staticmethod
	def M2():
		return Interval(2)

	@staticmethod
	def m3():
		return Interval(3)

	@staticmethod
	def M3():
		return Interval(4)

	@staticmethod
	def P4():
		return Interval(5)

	@staticmethod
	def TT():
		return Interval(6)

	@staticmethod
	def P5():
		return Interval(7)

	@staticmethod
	def m6():
		return Interval(8)

	@staticmethod
	def M6():
		return Interval(9)

	@staticmethod
	def m7():
		return Interval(10)

	@staticmethod
	def M7():
		return Interval(11)

	@staticmethod
	def P8():
		return Interval(12)

