// nil out jquery 
var Nil = require('./test_lib/nil.js').Nil;
global.$ = new Nil(); 
global.performance = new Nil();  // performance.now()

var assert = require('assert');
var Game = require('../../view/js/game.js');
var Card = require('../../view/js/card.js');

var cardJSON = {
	"answer" : "D",
	"deck_id" : 3,
	"card_id" : 555,
	"question" : "What is a descending major sixth of B?"
};

describe('Game', function() {
	var game;
	var card;

	beforeEach(function() {
		game = new Game(1, 2);
		card = new Card(cardJSON);
	});

	describe('constructor', function() {
		it('should initialize session_id', function () {
			assert.ok(game.session_id == 1);
		})
		it('should initialize deck_id', function () {
			assert.ok(game.deck_id == 2);
		})
	});

	describe('state', function() {
		it('should initially be \'waiting\'', function() {
			assert.equal(game.state, 'waiting');
		});

		it('should change to \'loading next question\' on loadNextQuestion()', function() {
			game.card = card;
			game.loadNextQuestion();
			assert.equal(game.state, 'loading next question');
		});
	});

	describe('methods', function () {
		it('handleCardData should add a card to the game', function () {
			assert.ok(game.card == undefined);
			game.handleCardData(cardJSON);
			assert.ok(game.card != undefined);
		});
	})
});