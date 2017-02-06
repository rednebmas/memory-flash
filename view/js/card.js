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
	time_to_correct: undefined,

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

	captureTimeToAnswer: function() {
		var now = performance.now();
		this.time_to_correct = (now - this.start_time) / 1000.0;
	},

	validateAnswer: function(answer) {
		if (this.answer_validator.validate(answer, this.answer)) {
			if (this.validation_state == 'unanswered') {
				this.captureTimeToAnswer();
			}
			this.validation_state = 'correct';
		} else {
			this.validation_state = 'incorrect';
		}
		console.log('card.validation_state = ' + this.validation_state);
	},
}.init(); }

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Card;