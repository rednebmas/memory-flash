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
    "scale": "Gb",
    "accidental": "b",
	"deck_id": 6,
	"card_id": 2
}

var intervalCard = {
	"question": "What is a perfect fifth of Db?",
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
            assert.equal(midiInput.output(), 'C E G');
        });

        it('should recognize the accidental of the card even if there is no scale', function() {
            game.card = new Card(intervalCard);
            midiInput.addNote(44);
            assert.equal(midiInput.output(), "Ab");
        });

        it('should recognize to the scale of the card', function() {
            game.card = card;
            midiInput.addNote(42);
            midiInput.addNote(47);
            midiInput.addNote(51);
            assert.equal(midiInput.output(), 'Gb Cb Eb');
        });
    });
    
    describe('properties', function() {
        beforeEach(function () {
            midiInput = new MIDIInput();
            game = new Game();
            card = new Card(gflatCard);
            game.card = card;
        });

        it('should have a scale (if using a card with a scale)', function() {
            assert.ok(midiInput.scale != undefined);
        });

        it('should have a chroma map', function() {
            var scale = midiInput.scale;
            assert.ok(midiInput.chromaMap != undefined);;
        });

        // it('should reset on calling check answer', function() {
        //     // need to test!
        // });
    });
});