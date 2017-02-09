// TODO: remove onMIDINotes from any other file in the project
// TODO: actually should be able to remove midiEnharmonicsValid from answer validators! what a pain haha.
// TODO: test performance of output()
var teoria = require('teoria');

var MIDIInput = function () { return {
	/** 
	Properties 
	**/

	onNotes: new Set(),
	chromaMap: undefined,
	_scale: undefined,

	/** 
	Getters and Setters 
	**/

	get scale() {
		this.parseScaleInformationIfNeeded();
		return this._scale;
	},
	set scale(scale) {
		this._scale = scale;
	},

    /**
	Methods
    **/

	init: function() {
		this.startListeningForMIDIEvents();
		return this;
	},

	parseScaleInformationIfNeeded: function() {
		if (this._scale == undefined && game.card.raw['scale'] != undefined) {
			this._scale = this.parseTeoriaScaleFromScaleName(game.card.raw['scale']);
			this.createChromaMap();
		}
	},

	parseTeoriaScaleFromScaleName: function(scaleName) {
		var split = scaleName.split(" ");
		var scale;
		if (split.length == 1) { // major
			var note = teoria.note(split[0]);
			scale = note.scale('major');
		}
		return scale;
	},

	createChromaMap: function() {
		this.chromaMap = {};
		this.scale.notes().forEach(function (note) {
			this.chromaMap[note.chroma()] = note;
		}, this);
	},

	startListeningForMIDIEvents: function() {
		// http://tangiblejs.com/posts/web-midi-music-and-show-control-in-the-browser
		var self = this;
		WebMidi.enable(function (err) {
			if (err) console.log("WebMidi could not be enabled");

			var input = WebMidi.inputs[0];
			if (input) {
				// Listening for a 'note on' message (on all channels) 
				input.addListener("noteon", "all", function (e) {
					self.addNote(e.note.number)
				});

				// Listening to other messages works the same way 
				input.addListener("noteoff", "all", function (e) {
					self.removeNote(e.note.number);
				});
			}
		});
	},

	addNote: function(midiNoteNumber) {
		this.onNotes.add(midiNoteNumber);
		this.addOutputToGameInput();
	},

	removeNote: function(midiNoteNumber) {
		this.onNotes.delete(midiNoteNumber);
		this.addOutputToGameInput();
	},

	output: function() {
		var notes = Array.from(this.onNotes);
		notes.sort(function (a, b) { return a - b; }); // javascript converts all array elements to strings by default! yay! \s
		notes = notes.map(function(note) {
			return teoria.note.fromMIDI(note);
		});
		notes = this.makeNotesRespectCardAccidental(notes);
		notes = this.makeNotesRespectCardScale(notes);

		var noteNames = notes.map(function(note) {
			return note.name().toUpperCase() + note.accidental();
		});

		return noteNames.join(' ');
	}, 

	makeNotesRespectCardAccidental: function(notes) {
		var cardAccidentalValue = game.card.accidental == "#" ? 1 : -1;
		notes = notes.map(function(note) {
			if (note.accidentalValue() == 0 || note.accidentalValue() == cardAccidentalValue) {
				return note;
			} else {
				var enharmonics = note.enharmonics(true); // true means enharmonics w/ only one accidental
				var filtered = enharmonics.filter(function(enharmonic) {
					return enharmonic.accidentalValue() == cardAccidentalValue;
				});
				return filtered[0];
			}
		});
		return notes;
	},

	// check each note and see if it is a scale degree,
	// if so just replace with correct scale degree
	makeNotesRespectCardScale: function(notes) {
		if (this.scale == undefined) return notes;

		var self = this;
		notes = notes.map(function(note) {
			if (note.chroma() in self.chromaMap) {
				return self.chromaMap[note.chroma()];
			} else {
				return note;
			}
		});

		return notes;
	},

	addOutputToGameInput: function() {
		$('#answer-input').val(this.output());
	}

}.init(); };

if (typeof module !== 'undefined' && module.exports) 
	module.exports = MIDIInput;