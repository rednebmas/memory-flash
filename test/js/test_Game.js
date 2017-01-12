// nil out jquery 
var Nil = require('./test_lib/nil.js').Nil;
global.$ = new Nil(); 

var assert = require('assert');
var Game = require('../../view/js/game.js').Game;

describe('Game', function() {
	var game = new Game();

	beforeEach(function() {
		game = new Game();
	});

	describe('state', function() {
		it('should initially be \'waiting\'', function() {
			assert.equal(game.state, 'waiting');
		});
	});
});