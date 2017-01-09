var onMIDINotes = new Set();

// http://tangiblejs.com/posts/web-midi-music-and-show-control-in-the-browser
WebMidi.enable(function(err) { 
	if (err) console.log("WebMidi could not be enabled");

	var input = WebMidi.inputs[0];

	if (input) {
		// Listening for a 'note on' message (on all channels) 
		input.addListener("noteon", "all",
			function(e) { 
				addNote(e.note.number)
			}
		);

		// Listening to other messages works the same way 
		input.addListener("noteoff", "all",
			function(e) { 
				removeNote(e.note.number);
			}
		);
	}
});

function addNote(noteNumber) {
	onMIDINotes.add(noteNumber);
	addCurrentNotesToInput();

	// correct
	if (answer_validator($('#answer-input').val(), card.answer)) {
		console.log('addNote: correct answer');
		checkAnswer();
	}
	else if (noteNotInAnswer(noteNumber)) {
		console.log('not in answer, mark incorrect')
		markIncorrect();
	}
}

function noteNotInAnswer(noteNumber) {
	var noteName = MIDIUtils.noteNumberToName(noteNumber);
	noteName = answerValidator_replaceFlatsWithSharps(noteName);
	var answers = card.answer.split('|');

	var noteInAnswer = false;
	for (answer in answers) {
		var parts = answer.split(' ');
		for (part in parts) {
			noteInAnswer = noteInAnswer || (part == noteName);
		}
	}

	return !noteInAnswer;
}

function removeNote(noteNumber) {
	onMIDINotes.delete(noteNumber);
	addCurrentNotesToInput();
}

function addCurrentNotesToInput() {
	var onMIDINoteNumbers = Array.from(onMIDINotes);
	onMIDINoteNumbers.sort(function(a,b){ return a - b; }); // javascript converts all array elements to strings by default! yay!
	var onMIDINoteNames = [];

	for (var i = 0; i < onMIDINoteNumbers.length; i++) {
		onMIDINoteNames.push(MIDIUtils.noteNumberToName(onMIDINoteNumbers[i]));
	}

	$('#answer-input').val(onMIDINoteNames.join(' '));
}