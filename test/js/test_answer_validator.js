var assert = require('assert');
var AnswerValidator = require('../../view/js/answer_validator.js');

describe('AnswerValidator', function() {
	describe('equals', function() {
		it('should return false if not equal', function () {
			var validator = AnswerValidator('equals');
			assert.ok(validator.validate('time flies', 'like a bannana') == false);
		});

		it('should ignore case', function () {
			var validator = AnswerValidator('equals');
			assert.ok(validator.validate('time flies', 'time FLIES'));
		})
	});
});
