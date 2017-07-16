var stockMultiPartCard = require('./test_lib/stock_multi_part_card.js');
var Nil = require('./test_lib/nil.js').Nil; 
global.WebMidi = new Nil(); // nil out WebMidi
global.$ = new Nil(); 
var assert = require('assert');
var MIDIInput = require('../../view/js/midi_input.js');
var Game = require('../../view/js/game.js');
var Card = require('../../view/js/card.js');

var gflatCard = {
    "question": "IV V I in Gb",
    "answer": "Gb Cb Eb→F Ab Db→Gb Bb Db",
    "scale": "Gb major",
    "accidental": "b",
	"deck_id": 6,
	"card_id": 2,
	"answer_validator": "multipleOptions_equals_midiEnharmonicsValid",
}

var cMajorCard = {
	"card_id": 415,
	"deck_id": 2,
	"question": "C",
	"answer": "C E G",
	"answer_validator": "equals",
	"accidental": "#",
	"scale": "C major",
	"template_path": "cards/chord.html",
	"template_data": { "chord_pretty_name": "C/E" }
};

var intervalCard = {
	"question": "What is an ascending perfect fifth of Db?",
	"answer": "Ab",
	"deck_id": 2,
	"card_id": 1,
	"answer_validator": "multipleOptions_equals_midiEnharmonicsValid",
    "accidental": "b"
}

describe('MIDIInput', function() {
    var midiInput, card;

    beforeEach(function () {
        midiInput = new MIDIInput();
        game = new Game();
        card = new Card(gflatCard);
        game.card = card;
    });

    describe('midi events', function() {
        it('should add the note to the set of notes', function() {
            assert.equal(midiInput.onNotes.size, 0);
            midiInput.addNote(36);
            assert.equal(midiInput.onNotes.size, 1);
        });

        it('should remove notes from the set of notes', function() {
            assert.equal(midiInput.onNotes.size, 0);
            midiInput.addNote(36);
            midiInput.removeNote(36);
            assert.equal(midiInput.onNotes.size, 0);
        });

        it('should check answer if wrong note and change game state to "partial - incorrect"', function() {
            midiInput.addNote(41);
            assert.equal(game.state, 'partial - incorrect');
        });

        it('should check answer on correct answer and change game state to "partial - correct"', function() {
            midiInput.addNote(42);
            midiInput.addNote(47);
            midiInput.addNote(51);
            assert.equal(game.state, 'partial - correct');
        });
    });

    describe('method', function() {
        it('currentAnswerIsCorrectAnswer should return true', function() {
            // can't use addNote because if we did, after the last check and move the game state
            midiInput.onNotes.add(42);
            midiInput.onNotes.add(47);
            midiInput.onNotes.add(51);
            midiInput.output = midiInput.calcOutput();
            assert.ok(midiInput.currentAnswerIsCorrectAnswer());
        });

        it('currentAnswerIsCorrectAnswer should return false', function() {
            midiInput.addNote(41);
            midiInput.addNote(47);
            midiInput.addNote(51);
            assert.ok(midiInput.currentAnswerIsCorrectAnswer() == false);
        });

        it('currentAnswerIsPartOfCorrectAnswer should return true', function() {
            midiInput.addNote(42);
            assert.ok(midiInput.currentAnswerIsPartOfCorrectAnswer());
        });

        it('currentAnswerIsPartOfCorrectAnswer should return false', function() {
            midiInput.addNote(41);
            assert.ok(midiInput.currentAnswerIsPartOfCorrectAnswer() == false);
        });
    });

    describe('output', function() {
        beforeEach(function () {
            midiInput = new MIDIInput();
            game = new Game();
            card = new Card(gflatCard);
            game.card = card;
        });

        it('should produce a string of notes', function() {
            game.card = new Card(stockMultiPartCard);
            midiInput.addNote(36);
            midiInput.addNote(40);
            midiInput.addNote(43);
            assert.equal(midiInput.output, 'C E G');
        });

        it('should recognize the accidental of the card even if there is no scale', function() {
            game.card = new Card(intervalCard);
            midiInput.addNote(44);
            assert.equal(midiInput.output, "Ab");
        });

        it('should recognize to the scale of the card', function() {
            game.card = card;
            midiInput.addNote(42);
            midiInput.addNote(47);
            midiInput.addNote(51);
            assert.equal(midiInput.output, 'Gb Cb Eb');
        });
    });
    
    describe('properties', function() {
        it('should have a scale (if using a card with a scale)', function() {
            assert.ok(midiInput.scale != undefined);
        });

        it('should have a chroma map', function() {
            var scale = midiInput.scale;
            assert.ok(midiInput.chromaMap != undefined);;
        });
    });

	describe('bugs', function () {
		it('should have output e# instead of f for f# scale', function () {
			var card = new Card({ "template_path": "cards/chord-progression/chord-progression.html", "card_id": 819, "template_data": { "root": "F#", "chords": [{ "template_path": "cards/chord-progression/chord-progression-inv-0.html", "symbol": "IV" }, { "template_path": "cards/chord-progression/chord-progression-inv-2.html", "symbol": "V" }, { "template_path": "cards/chord-progression/chord-progression-inv-1.html", "symbol": "I" }] }, "answer_validator": "equals", "deck_id": 8, "answer": "B D# F#→G# C# E#→A# C# F#", "scale": "F#", "accidental": "#", "question": "IV V I in F#" });
            game.card = card;
			assert.ok(midiInput.scale != undefined);
			assert.equal(midiInput.scale.tonic.name() + midiInput.scale.tonic.accidental(), 'f#');

            midiInput.addNote(53); // f, should output e# though
            assert.equal(midiInput.calcOutput(), 'E#');
		});

        it('should show Fb instead of E', function() {
            var card = new Card({"card_id":65,"deck_id":1,"question":"↓ M3 of A♭","answer":"Fb","answer_validator":"multipleOptions_equals_midiEnharmonicsValid","accidental":null,"scale":"Ab major","template_path":"cards/interval.html","template_data":{"interval":"M3","direction":"↓","note":"A♭"}});

            game.card = card;
            midiInput.addNote(52); // "e", should be Fb
            assert.equal(midiInput.calcOutput(), 'Fb');
		});
		
		it('should not error on chord cards', function() {
			game.card = new Card(cMajorCard);
			midiInput.addNote(52); // "e"
		});
	});
});