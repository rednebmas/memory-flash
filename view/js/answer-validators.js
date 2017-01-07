var answerValidator_equals = function(userAnswer, correctAnswer) {
	// Case insensitive
	return userAnswer.toLowerCase() == correctAnswer.toLowerCase();
}

var answerValidator_equals_case_sensitive = function(userAnswer, correctAnswer) {
	return userAnswer == correctAnswer;
}

var answerValidator_multipleOptions_meta = function(userAnswer, correctAnswer, validator) {
	var answers = correctAnswer.split('|');
	for (var i = answers.length - 1; i >= 0; i--) {
		if (answerValidator_equals(userAnswer, answers[i])) {
			return true;
		}
	}
	return false;
}

var answerValidator_multipleOptions_equals = function(userAnswer, correctAnswer) {
	return answerValidator_multipleOptions_meta(userAnswer, correctAnswer, answerValidator_equals);
}
