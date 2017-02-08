var assert = require('assert');
var Card = require('../../view/js/card.js');
// make performance.now() node compatible
global.performance = {};
global.performance.now = require('performance-now');

var cardJSON = {
	"answer" : "D",
	"deck_id" : 3,
	"card_id" : 555,
	"question" : "What is a descending major sixth of B?",
	"answer_validator" : "multipleOptions_equals_midiEnharmonicsValid"
};

var multiPartAnswerCardJSON = {
	"answer" : "C E G→C F A→B D G",
	"deck_id" : 6,
	"card_id" : 2,
	"question" : "Four Five One Progression in C",
	"answer_validator" : "multipleOptions_equals_midiEnharmonicsValid"
}

describe('Card', function() {
	var card;

	beforeEach(function() {
		card = new Card(cardJSON);
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

	describe('methods', function() {
		it('should reset the state on resetState()', function() {
			card = new Card(multiPartAnswerCardJSON);
			card.resetState();
			assert.equal(card.validation_state, 'unanswered');
			assert.equal(card.current_answer_part_index, 0);
			assert.equal(card.validation_states[0], 'unanswered');
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

		it('should change first attempt correct to false', function () {
			card.validateAnswer('Richard Feynman')
			assert.equal(card.first_attempt_correct, false);
		});

		it('should capture time to correct when answer is incorrect at first', function() {
			card.captureStartTime();
			card.validateAnswer('Richard Feynman')
			assert.ok(card.time_to_correct == undefined);
			card.validateAnswer(card.answer);
			assert.ok(card.time_to_correct != undefined && isNaN(card.time_to_correct) == false);
		});
	});

	describe('multipart answers', function() {
		beforeEach(function() {
			card = new Card(multiPartAnswerCardJSON);
		});

		it('should have an answers array if answer is multipart', function() {
			assert.ok(Array.isArray(card.answers));
		});

		it('should change current answer part index on correct answer', function() {
			card.validateAnswer('C E G');
			assert.equal(card.current_answer_part_index, 1);
		});

		it('should capture time to correct', function() {
			card.captureStartTime();
			card.validateAnswer('C E G');
			card.validateAnswer('C F A');
			card.validateAnswer('B D G');
			assert.ok(card.time_to_correct != undefined && isNaN(card.time_to_correct) == false);
		});

		describe('validation states', function() {
			it('should change to "correct" on correct answer', function() {
				card.validateAnswer('C E G');
				assert.equal(card.validation_states[0], 'correct');
			});

			it('should change to "incorrect" then to "correct but first attempt incorrect"', function() {
				card.validateAnswer('C E A');
				assert.equal(card.validation_states[0], 'incorrect');
				assert.equal(card.current_answer_part_index, 0);
				card.validateAnswer('C E G');
				assert.equal(card.validation_states[0], 'correct but first attempt incorrect');
			});
		});

		describe('validation state', function() {
			it ('should change to "partial - incorrect" then to "incorrect" when done answering', function() {
				assert.equal(card.validation_state, 'unanswered');
				card.validateAnswer('C E G');
				assert.equal(card.validation_state, 'partial - correct');
				card.validateAnswer('C Z A');
				assert.equal(card.validation_state, 'partial - incorrect');
				card.validateAnswer('C F A');
				card.validateAnswer('B D G');
				assert.equal(card.validation_state, 'incorrect');
			});

			it('should change to "partial - correct" then to "correct" when done answering', function() {
				card.validateAnswer('C E G');
				assert.equal(card.validation_state, 'partial - correct');
				card.validateAnswer('C F A');
				card.validateAnswer('B D G');
				assert.equal(card.validation_state, 'correct');
			});
		});
	});
});
