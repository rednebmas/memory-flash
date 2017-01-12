function Game() {
	// set(waiting, partially_correct, first_attempt_incorrect, correct)
	this.state = 'waiting';
}

if (typeof exports !== 'undefined') 
	exports.Game = Game;