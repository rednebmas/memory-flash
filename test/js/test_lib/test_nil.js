var assert = require('assert');
var Nil = require('./nil.js').Nil;

describe('Nil.js', function() {
	it('should chain expressions', function() {
		var nil = new Nil();
		assert.doesNotThrow(
			() => {
				nil.infinitelyChainsCalls().or.properties.withoutRepercussions();
			},
			Error
		);
	});

	it('should not throw on console.log()', function() {
		var nil = new Nil();
		assert.doesNotThrow(
			() => {
				console.log(nil);
			},
			Error
		);
	});
});