var Card = require('./card.js');

// this pattern allows getters and setters (http://stackoverflow.com/a/17606845/337934) and a constructor
// also see the last example from http://stackoverflow.com/a/21648197/337934
var Game = function(session_id, deck_id) { return { 
	/** 
	Properties 
	**/

	session_id: session_id,
	deck_id: deck_id,
	_state: 'waiting', // waiting, loading next question, partially_correct, first_attempt_incorrect, correct
	card: undefined,

	/** 
	Getters and Setters 
	**/

	get state() {
		return this._state;
	},
	set state(value) {
		this._state = value;
		switch (value) {
			case 'waiting':
				this.updateDisplayForWaiting();
				break;
		}
	},

    /**
	Methods
    **/

    init: function () {
    	this.bindSubmitAnswer();
    	return this;
    },

	bindSubmitAnswer: function() {
		$('#answer-input').focus();
		$("#submit-answer").click(function() {
			checkAnswer();
		});

		$('#answer-input').keypress(function(e) {
			if (e.which == 13) { // enter key pressed
				checkAnswer();
			}
		});
	},

	loadNextQuestion: function() {
		this.state = 'loading next question';

		var url = '/session/' + this.session_id + '/next_card';
		var data = { 
			'deck_id' : this.deck_id, 
			'previous_card_id' : this.card.card_id 
		};

		$.get(url, data, this.handleCardData)
		 .fail(function(xhr, status, error) {
			console.log('Error retrieving next card: ' + xhr);
		 });
	},

	handleCardData: function(data) {
		console.log(JSON.stringify(data));
		this.card = new Card(data);
		this.state = 'waiting';
	},

	updateDisplayForWaiting: function () {
		this.card.captureStartTime();
		$('.question').html(this.card.question);
		$('#submit-answer').attr('class', 'btn btn-primary');
		$('#correct-label').fadeOut();
	}
}.init(); }

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Game;