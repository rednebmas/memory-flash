// TODO: remove onMIDINotes from any other file in the project
// TODO: actually should be able to remove midiEnharmonicsValid from answer validators! what a pain haha.
// TODO: test performance of output()
var teoria = require('teoria');

var MIDIInput = function () {
	return {
		/** 
	Properties 
	**/

		onNotes: new Set(),
		chromaMap: undefined,
		_scale: undefined,
		output: undefined, // not a midi output
		input: undefined,

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

		init: function () {
			this.startWebMidi();
			return this;
		},

		parseScaleInformationIfNeeded: function () {
			if (
				this._scale == undefined &&
				game.state != 'loading next question' &&
				game.card.raw['scale'] != undefined
			) {
				this._scale = this.parseTeoriaScaleFromScaleName(game.card.raw['scale']);
				this.createChromaMap();
			}
		},

		parseTeoriaScaleFromScaleName: function (scaleName) {
			var split = scaleName.split(' ');
			var note = teoria.note(split[0]);
			var theScale;
			if (split.length == 1) {
				// major
				theScale = note.scale('major');
			} else if (split[1] == 'major') {
				theScale = note.scale('major');
			} else if (split[1] == 'minor') {
				theScale = note.scale('minor');
			}
			return theScale;
		},

		createChromaMap: function () {
			this.chromaMap = {};
			this._scale.notes().forEach(function (note) {
				this.chromaMap[note.chroma()] = note;
			}, this);
		},

		startWebMidi: function () {
			// http://tangiblejs.com/posts/web-midi-music-and-show-control-in-the-browser
			WebMidi.enable((err) => {
				if (err) {
					console.log('WebMidi could not be enabled');

					var urlSearchParams = new URLSearchParams(window.location.search);
					if (urlSearchParams.get('input_modality_id') != '1') {
						alert('Error: ' + err);
					}
					return;
				}

				WebMidi.addListener('connected', (e) => {
					this.populateInputList();
					this.listenToSavedMidiInputIfAvailable();
				});

				WebMidi.addListener('disconnected', (e) => {
					$('#midi-connected').css('display', 'none');
					this.populateInputList();
				});

				if (WebMidi.inputs.length > 0) {
					this.populateInputList();
					this.listenToSavedMidiInputIfAvailable();
				}
			});
		},

		listenToEventsFromInput: function (input) {
			if (!input) {
				this.input = undefined;
				return;
			}

			if (this.input) {
				this.input.removeListener();
			}

			this.input = input;
			$('#midi-input-dropdown-text').text(this.input.name);
			Cookies.set('midi-input-id', input.id);

			// Listening for a 'note on' message (on all channels)
			input.addListener('noteon', 'all', (e) => {
				this.addNote(e.note.number);
			});

			// Listening to other messages works the same way
			input.addListener('noteoff', 'all', (e) => {
				this.removeNote(e.note.number);
			});
		},

		listenToSavedMidiInputIfAvailable: function () {
			var midiInputID = Cookies.get('midi-input-id');
			if (!midiInputID) return;

			var input = WebMidi.getInputById(midiInputID);
			if (input) {
				this.listenToEventsFromInput(input);
			}
		},

		addNote: function (midiNoteNumber) {
			if (game.state == 'title card' && teoria.note.fromMIDI(midiNoteNumber).name() == 'c') {
				game.state = 'waiting';
				return;
			}

			this.onNotes.add(midiNoteNumber);
			this.output = this.calcOutput();
			this.addOutputToGameInput();
			this.checkAnswerIfNeeded();
		},

		checkAnswerIfNeeded: function () {
			if (this.currentAnswerIsCorrectAnswer()) {
				game.checkAnswer(this.output);
				if (game.state == 'loading next question') {
					this.scale = undefined;
				}
			} else if (this.currentAnswerIsPartOfCorrectAnswer() == false) {
				game.checkAnswer(this.output);
			}
		},

		currentAnswerIsPartOfCorrectAnswer: function (arguments) {
			var userAnswerParts = this.output.split(' ');
			var correctAnswerParts = this.currentCorrectAnswer().split(' ');
			var isSubset = true;
			userAnswerParts.forEach(function (userAnswerPart) {
				isSubset = isSubset & (correctAnswerParts.indexOf(userAnswerPart) >= 0);
			}, this);

			return isSubset == 1; // javascript bitwise operators return 0 or 1 instead of true/false
		},

		currentAnswerIsCorrectAnswer: function () {
			var userAnswer = this.output;
			return game.card.answer_validator.validate(userAnswer, this.currentCorrectAnswer());
		},

		currentCorrectAnswer: function () {
			var answer;
			if (game.card.answers != undefined) {
				if (game.card.current_answer_part_index == game.card.answers.length) {
					answer = game.card.answers[game.card.current_answer_part_index - 1];
				} else {
					answer = game.card.answers[game.card.current_answer_part_index];
				}
			} else {
				answer = game.card.answer;
			}
			return answer;
		},

		removeNote: function (midiNoteNumber) {
			this.onNotes.delete(midiNoteNumber);
			this.output = this.calcOutput();
			this.addOutputToGameInput();
		},

		clearOnNotes: function () {
			this.onNotes = new Set();
		},

		calcOutput: function () {
			var notes = Array.from(this.onNotes);
			notes.sort(function (a, b) {
				return a - b;
			}); // javascript converts all array elements to strings by default! yay! \s
			notes = notes.map(function (note) {
				return teoria.note.fromMIDI(note);
			});
			notes = this.makeNotesRespectCardAccidental(notes);
			notes = this.makeNotesRespectCardScale(notes);
			notes = this.makeNotesRespectCardAnswer(notes);

			var noteNames = notes.map((note) => {
				var name = note.name().toUpperCase() + note.accidental().replace('x', '##');
				if (game.card.raw['answer_validator'] == 'equals_octave') {
					name = name + note.octave();
				}
				return name;
			});

			return noteNames.join(' ');
		},

		makeNotesRespectCardAccidental: function (notes) {
			var cardAccidentalValue = game.card.accidental == '#' ? 1 : -1;
			notes = notes.map(function (note) {
				if (note.accidentalValue() == 0 || note.accidentalValue() == cardAccidentalValue) {
					return note;
				} else {
					var enharmonics = note.enharmonics(true); // true means enharmonics w/ only one accidental
					var filtered = enharmonics.filter(function (enharmonic) {
						return enharmonic.accidentalValue() == cardAccidentalValue;
					});
					return filtered[0];
				}
			});
			return notes;
		},

		// check each note and see if it is a scale degree,
		// if so just replace with correct scale degree
		makeNotesRespectCardScale: function (notes) {
			if (this.scale == undefined) return notes;

			var self = this;
			notes = notes.map(function (note) {
				if (note.chroma() in self.chromaMap) {
					return self.chromaMap[note.chroma()];
				} else {
					return note;
				}
			});

			return notes;
		},

		// at the moment this only works with single part answers
		makeNotesRespectCardAnswer: function (notes) {
			if (game.card.answers != undefined) return notes;

			var answerNotes = game.card.answer.split(' ');
			var answerNotesTeoria = answerNotes.map(teoria.note);
			var answerNotesChroma = answerNotesTeoria.map(function (note) {
				return note.chroma();
			});
			notes = notes.map(function (note) {
				var index = answerNotesChroma.indexOf(note.chroma());
				if (index >= 0) {
					var answerNoteTeoria = answerNotesTeoria[index];
					if (answerNoteTeoria.name() == note.name()) {
						return note;
					} else {
						return answerNoteTeoria;
					}
				} else {
					return note;
				}
			});

			return notes;
		},

		addOutputToGameInput: function () {
			$('#answer-input').val(this.output);
		},

		exists: function () {
			return this.input != undefined && this.input != null;
		},

		populateInputList: function () {
			var self = this;
			$('#midi-input-dropdown-list').empty();
			$.each(WebMidi.inputs, (i, input) => {
				$('<li/>')
					.append(
						$('<a/>', {
							html: input.name,
							class: 'dropdown-item',
							'midi-id': input.id,
							href: '#',
							click: (event) => {
								this.listenToEventsFromInput(
									WebMidi.getInputByName(event.target.innerText)
								);
							}
						})
					)
					.appendTo('#midi-input-dropdown-list');
			});
		}
	}.init();
};

if (typeof module !== 'undefined' && module.exports) module.exports = MIDIInput;
