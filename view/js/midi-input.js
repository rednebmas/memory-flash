var onMIDINotes = new Set();

WebMidi.enable(function(err) { 
	if (err) console.log("WebMidi could not be enabled");

	var input = WebMidi.inputs[0];

	if (input) {
		// Listening for a 'note on' message (on all channels) 
		input.addEventListener('noteon', "all",
			function(e) { 
				console.log(e);
			}
		);

		// Listening to other messages works the same way 
		input.addEventListener('noteoff', "all",
			function(e) { 
				console.log(e);
			}
		);
	}
});

function addNote(noteNumber) {
	onMIDINotes.add(noteNumber);
	addCurrentNotesToInput();
}

function removeNote(noteNumber) {
	onMIDINotes.delete(noteNumber);
}

function addCurrentNotesToInput() {
	var onMIDINoteNumbers = Array.from(onMIDINotes);
	onMIDINoteNumbers.sort();
	var onMIDINoteNames = [];

	for (var i = 0; i < onMIDINoteNumbers.length; i++) {
		onMIDINoteNames.push(MIDIUtils.noteNumberToName(onMIDINoteNumbers[i]));
	}

	$('#answer-input').val(onMIDINoteNames.join(' '));
}