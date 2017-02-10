import re
import math
from math import floor
from model.objects.accidental import Accidental

class Note:
	A4_FREQUENCY = 440.0
	TWO_TO_THE_ONE_OVER_TWELVE = 1.059463094359295264561825294

	def __init__(self, name=None, freq=None, accidental=None):
		self._accidental = None
		if name:
			self.init_with_name(name)
		elif freq:
			self.init_with_freq(freq, accidental)

	def init_with_freq(self, freq, accidental=None):
		self.freq = freq
		self.name, self.octave = Note.name_octave_for_freq(freq)
		if accidental == Accidental.flat and self.isaltered(): self.name = Note.sharp_to_flat(self.name)
		self.pretty_name = self.name.replace('#', '♯').replace('b','♭')
		self.name_octave = self.name + str(self.octave)
		self.half_steps_from_a4 = Note.half_steps_from_a4(self.name, self.octave)

	def init_with_name(self, name):
		name = name[0].upper() + name[1:] if name[0].islower() else name
		self.name, self.octave = Note.parse_name_and_octave(name)
		self.name_octave = self.name + str(self.octave)
		self.pretty_name = self.name.replace('#', '♯').replace('b','♭')
		self.half_steps_from_a4 = Note.half_steps_from_a4(self.name, self.octave)
		self.freq = Note.frequency_for_note_with_half_steps_from_a4(self.half_steps_from_a4)

	def transposed(self, interval, accidental=None):
		# scale = Scale(self.name)
		new_half_steps_from_a4 = self.half_steps_from_a4 + interval.half_steps
		if accidental is None: 
			accidental = self.accidental
		return Note(freq=Note.frequency_for_note_with_half_steps_from_a4(new_half_steps_from_a4), accidental=accidental)

	def enharmonics(self):
		converter = Note.enharmonic_converter()
		if self.name not in converter: return Note(name=self.name_octave)

		octave_str = str(self.octave)
		flat = Note(name=converter[self.name][0]+octave_str)
		sharp = Note(name=converter[self.name][1]+octave_str)
		return flat, sharp

	def isaltered(self):
		return '#' in self.name or 'b' in self.name

	@property
	def accidental(self):
		if self._accidental is None:
			if '#' in self.name:
				self._accidental = Accidental.sharp
			elif 'b' in self.name:
				self._accidental = Accidental.flat
			else:
				self._accidental = Accidental.natural
		return self._accidental

	def __str__(self):
		return self.name_octave

	def __eq__(self, other):
		"""Override the default Equals behavior"""
		if isinstance(other, self.__class__):
			return other.name_octave == self.name_octave
		return False

	def __ne__(self, other):
		"""Define a non-equality test"""
		return not self.__eq__(other)

	@staticmethod
	def parse_name_and_octave(full_name):
		""" If name does not contain octave, returns 4 """
		match = re.search(r'([ABCDEFG][#b]?)(\d+)?', full_name)
		if match:
			name = match.group(1)  

			if match.group(2):
				octave = match.group(2)
			else:
				octave = '4'
		else:
			raise Exception('Invalid note name ' + full_name)
		return name, int(octave)

	############
	## Theory ##
	############

	@staticmethod 
	def freq_from_name_octave(name, octave):
		half_steps = Note.half_steps_from_a4(Note.flat_to_sharp(name), octave)
		return Note.frequency_for_note_with_half_steps_from_a4(half_steps)

	@staticmethod 
	def name_octave_for_freq(freq):
		centDiff = 1200.0 * math.log(freq / Note.A4_FREQUENCY, 2)
		noteDiff = floor(centDiff / 100.0);

		matlabModulus = centDiff - 100.0 * floor(centDiff / 100.0)
		if matlabModulus > 50:
		    noteDiff = noteDiff + 1;

		note_names = Note.names()

		centsOff = centDiff - noteDiff * 100
		noteNumber = noteDiff + 9 + 12 * 4
		octave = int(floor(noteNumber / 12))
		place = int(noteNumber % 12) + 1

		name = note_names[place - 1]
		return name, octave

	@staticmethod
	def frequency_for_note_with_half_steps_from_a4(half_steps):
		return Note.A4_FREQUENCY * (Note.TWO_TO_THE_ONE_OVER_TWELVE ** half_steps)

	@staticmethod
	def half_steps_from_a4(name, octave):
		return Note.half_steps_away_from_a4_to_note_in_4th_octave(name) + 12 * (octave - 4)

	@staticmethod
	def half_steps_away_from_a4_to_note_in_4th_octave(note): 
		if note == "B#": note = "C"
		elif note == "E#": note = "F"
		constants = [-9, -8, -7, -6, -5, -4, -3, -2, -1, 0, 1, 2]
		return constants[Note.names().index(Note.flat_to_sharp(note))]

	###############
	## Constants ##
	###############

	@staticmethod
	def notes():
		return [Note(name=name) for name in Note.names()]

	@staticmethod
	def names():
		return ["C", "C#", "D" , "D#" , "E" , "F" , "F#", "G" , "G#" , "A" , "A#" , "B"]

	@staticmethod
	def names_with_enharmonics():
		return ["C", "C#", "Db", "D" , "D#" , "Eb", "E" , "F" , "F#", "Gb", "G" , "G#" , "Ab", "A" , "A#" , "Bb", "B"]		

	@staticmethod
	def flat_to_sharp(note):
		converter = {
			"Bb" : "A#",
			"Eb" : "D#",
			"Ab" : "G#",
			"Db" : "C#",
			"Gb" : "F#",
			"Cb" : "B",
			"Fb" : "E"
		}
		return converter[note] if note in converter else note

	@staticmethod
	def sharp_to_flat(note):
		converter = {
			"A#" : "Bb",
			"D#" : "Eb",
			"G#" : "Ab",
			"C#" : "Db",
			"F#" : "Gb",
		}
		return converter[note] if note in converter else note

	@staticmethod
	def enharmonic_converter():
		return {
			"C#" : ["Db", "C#"],
			"D#" : ["Eb", "D#"],
			"F#" : ["Gb", "F#"],
			"G#" : ["Ab", "G#"],
			"A#" : ["Bb", "A#"],

			"Db" : ["Db", "C#"],
			"Eb" : ["Eb", "D#"],
			"Gb" : ["Gb", "F#"],
			"Ab" : ["Ab", "G#"],
			"Bb" : ["Bb", "A#"],
		}
