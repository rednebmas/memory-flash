var AnswerValidator = function(validator_string) { return {
	/**
	Properties
	**/

	validator: undefined,

	/**
	Methods
	**/

	init: function() {
		this.validator = this[validator_string];
		return this;
	},

	validate: function(userAnswer, correctAnswer) {
		return this.validator(userAnswer, correctAnswer);
	},

	/** Validators **/

	equals: function (userAnswer, correctAnswer) {
		return userAnswer.toLowerCase() == correctAnswer.toLowerCase();
	},

	equals_octave: function (userAnswer, correctAnswer) {
		if (userAnswer.toLowerCase() != correctAnswer.toLowerCase() && game.input_modality_id == "1") {
			correctAnswer = correctAnswer.replace(/\d/g, "");
		}

		return userAnswer.toLowerCase() == correctAnswer.toLowerCase();
	},

	multipleOptions_meta: function(userAnswer, correctAnswer, validator) {
		var answers = correctAnswer.split('|');
		for (var i = answers.length - 1; i >= 0; i--) {
			if (this.equals(userAnswer, answers[i])) {
				return true;
			}
		}
		return false;
	},

	multipleOptions_equals: function(userAnswer, correctAnswer) {
		return this.multipleOptions_meta(userAnswer, correctAnswer, this.equals);
	},

	multipleOptions_equals_midiEnharmonicsValid: function(userAnswer, correctAnswer) {
		// if (onMIDINotes.size > 0) {
		// 	correctAnswer = this.replaceFlatsWithSharps(correctAnswer);
		// 	userAnswer = this.replaceFlatsWithSharps(userAnswer);
		// 	return this.multipleOptions_equals(userAnswer, correctAnswer);
		// } 

		return this.multipleOptions_equals(userAnswer, correctAnswer);
	},

	/** Helper **/

	replaceFlatsWithSharps: function(str) {
		for (key in enharmonicConverter) {
			str = str.replace(key, enharmonicConverter[key]);
		}
		return str;
	}
}.init(); };

if (typeof module !== 'undefined' && module.exports) 
	module.exports = AnswerValidator;