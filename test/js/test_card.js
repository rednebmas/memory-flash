var assert = require('assert');
var Card = require('../../view/js/card.js');

var cardJSON = {
	"answer" : "D",
	"deck_id" : 3,
	"card_id" : 555,
	"question" : "What is a descending major sixth of B?",
	"answer_validator" : "multipleOptions_equals_midiEnharmonicsValid"
};

describe('Card', function() {
	var card;

	beforeEach(function() {
		card = new Card(cardJSON);
		// causes throw in node
		card.captureTimeToAnswer = function() {};
	});

	describe('constructor', function() {
		it('should have a question', function() {
			assert.equal(card.question, cardJSON['question']);
		});

		it('should have an array for property answers', function() {
			assert.equal(card.answer, cardJSON['answer']);
		});

		it('should have a deck_id', function() {
			assert.equal(card.deck_id, cardJSON['deck_id'])
		});

		it('should have a card_id', function() {
			assert.equal(card.card_id, cardJSON['card_id'])
		});

		it('first_attempt_correct should be true', function() {
			assert.ok(card.first_attempt_correct);
		});

		it('should have an answer validator', function() {
			assert.ok(card.answer_validator != undefined);
			assert.ok(card.answer_validator != cardJSON['answer_validator']);
		});

		it('should have an initial answer validation state', function () {
			assert.equal(card.validation_state, 'unanswered');
		});
	});

	describe('answer validation', function () {
		beforeEach(function() {
			global.onMIDINotes = Array();
		});

		it('should change validation state to correct', function () {
			assert.equal(card.validation_state, 'unanswered')
			card.validateAnswer(cardJSON['answer'])
			assert.equal(card.validation_state, 'correct');
		});

		it('should change validation state to incorrect', function () {
			assert.equal(card.validation_state, 'unanswered')
			card.validateAnswer('Richard Feynman')
			assert.equal(card.validation_state, 'incorrect');
		});
	});
});
