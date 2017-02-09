var onMIDINotes = new Set();

// http://tangiblejs.com/posts/web-midi-music-and-show-control-in-the-browser
WebMidi.enable(function(err) {
	if (err) console.log("WebMidi could not be enabled");

	var input = WebMidi.inputs[0];
	if (input) {
		// Listening for a 'note on' message (on all channels) 
		input.addListener("noteon", "all", function (e) {
			addNote(e.note.number)
		});

		// Listening to other messages works the same way 
		input.addListener("noteoff", "all", function (e) {
			removeNote(e.note.number);
		});
	}
});

function replaceFlatsWithSharps(str) {
	for (key in enharmonicConverter) {
		str = str.replace(key, enharmonicConverter[key]);
	}
	return str;
}

function addNote(noteNumber) {
	onMIDINotes.add(noteNumber);
	addCurrentNotesToInput();

	var userAnswer = $('#answer-input').val();
	var answer;
	// get answer
	if (game.card.answers != undefined) {
		answer = game.card.answers[game.card.current_answer_part_index];
	} else {
		answer = game.card.answer;
	}

	// correct
	if (game.card.answer_validator.validate(userAnswer, answer)) 
	{
		console.log('addNote: correct answer');
		game.checkAnswer(userAnswer);
	}
	else if (noteNotInAnswer(noteNumber, answer)) 
	{
		console.log('not in answer, mark incorrect')
		game.checkAnswer(userAnswer);
	} else {
		console.log('note ' + MIDIUtils.noteNumberToName(noteNumber) + ' in answer, not complete');
	}
}

function noteNotInAnswer(noteNumber, answer) {
	var noteName = MIDIUtils.noteNumberToName(noteNumber);
	noteName = replaceFlatsWithSharps(noteName);
	var answers = answer.split('|');

	var noteInAnswer = false;
	for (var i = 0; i < answers.length; i++) {
		var answer = answers[i];
		var parts = answer.split(' ');
		for (var j = 0; j < parts.length; j++) {
			var part = parts[j];
			part = replaceFlatsWithSharps(part);
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
	var accidental = game.card.accidental;
	console.log(accidental);
	var onMIDINoteNumbers = Array.from(onMIDINotes);
	onMIDINoteNumbers.sort(function(a,b){ return a - b; }); // javascript converts all array elements to strings by default! yay!
	var onMIDINoteNames = [];

	for (var i = 0; i < onMIDINoteNumbers.length; i++) {
		var noteName = MIDIUtils.noteNumberToName(onMIDINoteNumbers[i])
		if (accidental == 'b' && noteName.length == 2) {
			noteName = enharmonicConverter[noteName];
		}
		onMIDINoteNames.push(noteName);
	}

	$('#answer-input').val(onMIDINoteNames.join(' '));
}