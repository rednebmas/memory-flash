// based code from https://github.com/sole/MIDIUtils/blob/master/src/MIDIUtils.js
var enharmonicConverter = {
	"Db" : "C#",
	"Eb" : "D#",
	"Gb" : "F#",
	"Ab" : "G#",
	"Bb" : "A#",

	"C#" : "Db",
	"D#" : "Eb",
	"F#" : "Gb",
	"G#" : "Ab",
	"A#" : "Bb",
}

var MIDIUtils = {	
	noteNameToNoteNumber: function(name) {
		return this.noteMap[name];
	},

	noteNumberToFrequency: function(note) {
		return 440.0 * Math.pow(2, (note - 69.0) / 12.0);
	},

	noteNumberToName: function(note) {
		return this.noteNumberMap[note];
	},

	noteNumberToOctave: function(note) {

	},

	frequencyToNoteNumber: function(f) {
		return Math.round(12.0 * getBaseLog(f / 440.0, 2) + 69);
	},

	noteMap: {},
	noteNumberMap: [],
	noteOctaveMap: [],
	notes: [ "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B" ],

	onLoad: function() {
		for (var i = 0; i < 127; i++) {
			var index = i,
				key = this.notes[index % 12],
				octave = ((index / 12) | 0) - 1; // MIDI scale starts at octave = -1

			this.noteMap[key] = i;
			this.noteNumberMap[i] = key;
			this.noteOctaveMap[i] = octave;
		}
	},

	getBaseLog: function(value, base) {
		return Math.log(value) / Math.log(base);
	}
};

MIDIUtils.onLoad();