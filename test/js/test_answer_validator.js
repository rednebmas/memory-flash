var assert = require('assert');
var AnswerValidator = require('../../view/js/answer_validator.js');

describe('AnswerValidator', function() {
	describe('equals', function() {
		it('should have a validator', function() {
			var validator = AnswerValidator('equals');
			assert.ok(validator.validator != undefined);
		});

		it('should ignore case', function () {
			var validator = AnswerValidator('equals');
			assert.ok(validator.validate('Case Insensitive', 'case insensitive'));
		})

		it('should return false if not equal', function () {
			var validator = AnswerValidator('equals');
			assert.ok(validator.validate('time flies', 'like a bannana') == false);
		});
	});

	describe('multipleOptions_equals_midiEnharmonicsValid', function() {
		beforeEach(function() {
			global.onMIDINotes = Array();
		});
		
		it('should have a validator', function() {
			var validator = AnswerValidator('multipleOptions_equals_midiEnharmonicsValid');
			assert.ok(validator.validator != undefined);
		});
		it('should return true for regular ol\' equals', function() {
			var validator = AnswerValidator('multipleOptions_equals_midiEnharmonicsValid');
			assert.ok(validator.validate('Case Insensitive', 'case insensitive'));
		});
	})
});
