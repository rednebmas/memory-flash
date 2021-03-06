var AnswerValidator = require('./answer_validator.js');

// https://stackoverflow.com/a/5790850/337934
Function.prototype.getHashCode = (function(id) {
    return function() {
        if (!this.hashCode) {
            this.hashCode = '<hash|#' + (id++) + '>';
        }
        return this.hashCode;
    }
}(0));

var Card = function(json) { return {
	/**
	Properties
	**/

	first_attempt_correct: true,
	validation_state: 'unanswered', // unanswered, incorrect, correct, partial - correct, partial - incorrect
	question: json['question'],
	answer: json['answer'],
	deck_id: json['deck_id'],
	card_id: json['card_id'],
	answer_validator: undefined,
	accidental: undefined,
	time_to_correct: undefined,
	raw: json,
	/** multipart **/
	current_answer_part_index: 0,
	validation_states: undefined,
	listeners: {},

	/**
	Methods
	**/

	init: function() {
		this.answer_validator = AnswerValidator(json['answer_validator']);
		if ('accidental' in json) {
			this.accidental = json['accidental'];
		}
		if (json['answer'].includes('→')) { // if multipart answer
			this.answers = json['answer'].split('→');
			this.validation_states = Array(this.answers.length);
			this.validation_states.fill("unanswered");
		}
		return this;
	},

	captureStartTime: function() {
		this.start_time = performance.now();
	},

	captureTimeToCorrect: function() {
		var now = performance.now();
		this.time_to_correct = (now - this.start_time) / 1000.0;
		console.log(this.time_to_correct + 's captured for time to correct.');
	},

	validateAnswer: function(userAnswer) {
		// if multipart use multipart answer validation
		if (this.answers != undefined) {
			this.validateMultiPartAnswer(userAnswer);
			return;
		}

		if (this.answer_validator.validate(userAnswer, this.answer)) {
			this.captureTimeToCorrect();
			this.validation_state = 'correct';
		} else {
			this.validation_state = 'incorrect';
			this.first_attempt_correct = false;
		}
		console.log('card.validation_state = ' + this.validation_state);
	},

	validateMultiPartAnswer: function(userAnswer) {
		var answerPart = this.answers[this.current_answer_part_index];
		if (this.answer_validator.validate(userAnswer, answerPart)) 
		{
			if (this.validation_state == 'unanswered' || this.validation_state == 'incorrect') 
			{
				this.validation_state = 'partial - correct';
			} 

			var currentPartValidationState = this.validation_states[this.current_answer_part_index];
			if (currentPartValidationState == 'unanswered') 
			{
				this.validation_states[this.current_answer_part_index] = 'correct';
			} 
			else if (currentPartValidationState == 'correct but first attempt incorrect') 
			{
				this.validation_states[this.current_answer_part_index] = 'correct';
			}
			else if (currentPartValidationState == 'incorrect') 
			{
				this.validation_states[this.current_answer_part_index] = 'correct but first attempt incorrect';
			}
			console.log('card.validation_states = [ ' + this.validation_states.join(', ') + ' ]');

			this.current_answer_part_index += 1;
			this.callListener('movedToNextAnswerPart');
			if (this.current_answer_part_index == this.answers.length) // was last answer
			{ 
				this.validation_state = this.allAnswersCorrect() ? "correct" : "incorrect";
				if (this.validation_state == 'correct') {
					this.captureTimeToCorrect();
				} else {
					this.current_answer_part_index = 0;
					this.validation_states.fill("unanswered");
				}
			}
		} else {
			this.first_attempt_correct = false;
			this.validation_state = 'partial - incorrect';
			this.validation_states[this.current_answer_part_index] = 'incorrect';
			console.log('card.validation_states = [ ' + this.validation_states.join(', ') + ' ]');
		}
		console.log('card.validation_state = ' + this.validation_state);
	},

	allAnswersCorrect: function() {
		return this.validation_states.reduce(function (accumulator, currentValue) {
			return accumulator & (currentValue == "correct");
		}, true);
	},

	getAnswer: function () {
		if (this.answers == undefined) {
			return this.answer;
		} else {
			return this.answers[this.current_answer_part_index];
		}
	},

	addEventListener: function(name, func) {
		var callbacks;
		if (name in this.listeners) {
			callbacks = this.listeners[name];
		} else {
			callbacks = {}
		}

		callbacks[func.getHashCode()] = func;

		// movedToNextAnswerPart
		this.listeners[name] = callbacks;
	},

	callListener: function(name) {
		if ((name in this.listeners) == false) {
			return;
		}

		for (var key in this.listeners[name]) {
			this.listeners[name][key]();
		}
	},

	wasCorrect: function() {
		var session = this.raw.session;
		if (!session) {
			return false;
		}

		var prev_time_to_correct = this.raw.prev_time_to_correct;
		return prev_time_to_correct <= session.median && this.raw.prev_first_attempt_correct;
	}
}.init(); }

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Card;