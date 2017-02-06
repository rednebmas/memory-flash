var AnswerValidator = require('./answer_validator.js');

var Card = function(json) { return {
	/**
	Properties
	**/

	first_attempt_correct: true,
	validation_state: 'unanswered',
	question: json['question'],
	answer: json['answer'],
	deck_id: json['deck_id'],
	card_id: json['card_id'],
	answer_validator: undefined,
	accidental_type: undefined,

	/**
	Methods
	**/

	init: function() {
		this.answer_validator = AnswerValidator(json['answer_validator']);
		if ('accidental_type' in json) {
			this.accidental_type = json['accidental_type'];
		}
		return this;
	},

	captureStartTime: function() {
		this.start_time = performance.now();
	},

	validateAnswer: function(answer) {
		if (this.answer_validator.validate(answer, this.answer)) {
			this.validation_state = 'correct';
		} else {
			this.validation_state = 'incorrect';
		}
		console.log('card.validation_state = ' + this.validation_state);
	}
}.init(); }

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Card;