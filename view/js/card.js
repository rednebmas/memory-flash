var Card = function(json) { return {
	/**
	Properties
	**/

	question: json['question'],
	answers: json['answer'].split('|'),
	deck_id: json['deck_id'],
	card_id: json['card_id'],
	first_attempt_correct: true,

	/**
	Methods
	**/

	init: function() {
		if ('accidental_type' in json) {
			this.accidental_type = json['accidental_type'];
		}
		return this;
	},

	captureStartTime: function() {
		this.startTime = performance.now();
	}
}.init(); }

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Card;