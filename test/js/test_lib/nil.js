/*
The Nil object behaves similarily to nil in Objective-C. You can infinitely 
chain calls or property accessors on it and it will never throw an exception.
I developed this for unit testing.

Example usage:
	var nil = new Nil();
	console.log(nil.infinitelyChainsCalls().or.properties.withoutRepercussions());

Based on code from http://stackoverflow.com/a/29723887/337934
Proxy documentation: https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Proxy
*/

var Nil = function() {
	var handler = {
		get: function(target, name) {
			// compatibility for Node.js, prevents "Maximum call stack size exceeded" exception
			if (typeof name == 'symbol' 
				&& name.toString() == 'Symbol(util.inspect.custom)') 
			{
				return function() { return '    nil.js instance was called in console.log() statement'; };
			}

			return new Proxy(function(){}, this);
		},
		apply: function(target, thisArg, argumentsList) {
			return new Proxy(function(){}, this);
		}
	};

	return new Proxy(function() {}, handler);
};

// for node.js
if (typeof module.exports !== 'undefined') 
	module.exports.Nil = Nil;
