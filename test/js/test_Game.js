// nil out jquery 
var Nil = require('./test_lib/nil.js').Nil;
global.$ = new Nil(); 
global.WebMidi = new Nil(); 
global.metronome = new Nil(); 
// make performance.now() node compatible
global.performance = {};
global.performance.now = require('performance-now');

var assert = require('assert');
var Game = require('../../view/js/game.js');
var Card = require('../../view/js/card.js');
global.midiInput.exists = function() { return false; };

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
		beforeEach(function() {
			game.card = card;
		});

		it('should initially be \'waiting\'', function() {
			assert.equal(game.state, 'waiting');
		});

		it('should change to \'loading next question\' on loadNextQuestion()', function() {
			game.card = card;
			game.loadNextQuestion();
			assert.equal(game.state, 'loading next question');
		});
	});

	describe('checkAnswer', function () {
		beforeEach(function() {
			game.card = card;
		});

		it('should change state to loading next question if answer was correct', function() {
			assert.equal(game.state, 'waiting');
			game.checkAnswer(card.answer);
			assert.equal(game.state, 'loading next question');
		});

		it('should change state to "incorrect" if answer was incorrect', function() {
			assert.equal(game.state, 'waiting');
			game.checkAnswer('smile breathe and go slowly');
			assert.equal(game.state, 'incorrect');
		});

		it('should change state to "incorrect" then to "correct first attempt incorrect", ' + 
			'and finally to "loading next question" after calling checkAnswer again', function() {
			assert.equal(game.state, 'waiting');
			game.checkAnswer('smile breathe and go slowly');
			assert.equal(game.state, 'incorrect');
			game.checkAnswer(card.answer);
			assert.equal(game.state, 'correct but first attempt incorrect');
			game.checkAnswer(card.answer);
			assert.equal(game.state, 'loading next question');
		});
	});

	describe('methods', function () {
		it('handleCardData should add a card to the game', function () {
			assert.ok(game.card == undefined);
			game.handleCardData(cardJSON);
			assert.ok(game.card != undefined);
		});
	});

	describe('mutlipart answers', function() {
		beforeEach(function() {
			card = new Card(multiPartAnswerCardJSON);
			game.card = card;
		});

		it('should change state to "partial - correct" after correctly answering a question', function() {
			game.checkAnswer('C E G');
			assert.equal(game.state, 'partial - correct');
		});

		it('should change state to "partial - incorrect" after answering a question', function() {
			game.checkAnswer('C A G');
			assert.equal(game.state, 'partial - incorrect');
		});

		it('should change state to "loading next question" after correctly answering all question parts', function() {
			game.checkAnswer('C E G');
			game.checkAnswer('C F A');
			game.checkAnswer('B D G');
			assert.equal(game.state, 'loading next question');
		});

		it('should change state to "waiting" after incorrectly answering ' + 
		   'one of the questions and completing the card', function() {
			game.checkAnswer('C E G');
			game.checkAnswer('C L A');
			game.checkAnswer('C F A');
			game.checkAnswer('B D G');
			assert.equal(game.state, 'waiting');
		});

		it('should allow you move on after repeating the answer after getting it incorrect', function() {
			console.log('C E G');
			game.checkAnswer('C E G');

			console.log('C L A');
			game.checkAnswer('C L A');

			console.log('C F A');
			game.checkAnswer('C F A');

			assert.equal(game.state, 'partial - incorrect');

			console.log('B D G');
			game.checkAnswer('B D G');

			assert.equal(game.state, 'waiting');
			
			console.log('C E G');
			game.checkAnswer('C E G');

			console.log('C F A');
			game.checkAnswer('C F A');

			console.log('B D G');
			game.checkAnswer('B D G');

			assert.equal('correct but first attempt incorrect', game.state);
		});

		it('should allow you move on after repeating the answer after getting it incorrect multiple times', function() {
			game.checkAnswer('C E G');
			game.checkAnswer('C L A');
			game.checkAnswer('C F A');
			assert.equal(game.state, 'partial - incorrect');
			game.checkAnswer('B D G');
			assert.equal(game.state, 'waiting');
			game.checkAnswer('C E G');
			game.checkAnswer('C L A');
			game.checkAnswer('C F A');
			assert.equal(game.state, 'partial - incorrect');
			game.checkAnswer('B D G');
			assert.equal(game.state, 'waiting');
			game.checkAnswer('C E G');
			game.checkAnswer('C F A');
			game.checkAnswer('B D G');
			assert.equal(game.state, 'correct but first attempt incorrect');
			game.checkAnswer('B D G');
			assert.equal(game.state, 'loading next question');
		});
	});
});