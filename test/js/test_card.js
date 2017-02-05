var assert = require('assert');
var Card = require('../../view/js/card.js');

var cardJSON = {
	"answer" : "D",
	"deck_id" : 3,
	"card_id" : 555,
	"question" : "What is a descending major sixth of B?"
};

describe('Card', function() {
	var card;

	beforeEach(function() {
		card = new Card(cardJSON);
	});

	describe('the constructor', function() {
		it('should have a question', function() {
			assert.equal(card.question, cardJSON['question']);
		});

		it('should have an array for property answers', function() {
			assert.ok(Array.isArray(card.answers));
		});

		it('should have a deck_id', function() {
			assert.equal(card.deck_id, cardJSON['deck_id'])
		});

		it('should have a card_id', function() {
			assert.equal(card.card_id, cardJSON['card_id'])
		});

		it('first_attempt_correct should be true', function() {
			assert.ok(card.first_attempt_correct);
		})
	});
});
