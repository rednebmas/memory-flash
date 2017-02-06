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
	_card: undefined,

	/** 
	Getters and Setters 
	**/

	get state() {
		return this._state;
	},
	set state(state) {
		this._state = state;
		switch (state) {
			case 'waiting':
				this.updateViewForStateWaiting();
				break;
		}
	},
		
	get card() {
		return this._card;
	},
	set card(card) {
		this._card = card;
		$('.question').html(card.question);
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
			'previous_card_id' : this.card ? this.card.card_id : 0
		};

		var self = this;
		$.get(url, data, function(data) {
			self.handleCardData(data);
		})
		.fail(function(xhr, status, error) {
			console.log('Error retrieving next card: ' + xhr);
		});
	},

	handleCardData: function(data) {
		console.log(JSON.stringify(data));
		this.card = new Card(data);
		this.state = 'waiting';
	},

	updateViewForStateWaiting: function () {
		this.card.captureStartTime();
		$('#submit-answer').attr('class', 'btn btn-primary');
		$('#correct-label').fadeOut();
	}
}.init(); };

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Game;

// hook into the webapp
if (typeof window !== 'undefined')
	window.Game = Game;
