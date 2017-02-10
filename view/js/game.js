var Card = require('./card.js');
var MIDIInput = require('./midi_input.js');
midiInput = new MIDIInput();

// this pattern allows getters and setters (http://stackoverflow.com/a/17606845/337934) and a constructor
// also see the last example from http://stackoverflow.com/a/21648197/337934
var Game = function(session_id, deck_id) { return { 
	/** 
	Properties 
	**/

	session_id: session_id,
	deck_id: deck_id,
	// waiting, loading next question, partial - correct, partial - incorrect, incorrect, correct but first attempt incorrect
	_state: 'waiting', 
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
			case 'incorrect':
				this.updateViewForStateFirstAttemptIncorrect();
				break;
			case 'correct but first attempt incorrect':
				this.updateViewForStateCorrectButFirstAttemptIncorrect();
				break;
			case 'loading next question':
				// this.updateViewForStateLoadingNextQuestion();
				break;
			case 'partial - correct':
			case 'partial - incorrect':
				this.updateViewForStatePartial();
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
		var self = this;

		$('#answer-input').focus();
		$("#submit-answer").click(function() {
			self.checkAnswer($('#answer-input').val());
		});

		$('#answer-input').keypress(function(e) {
			if (e.which == 13) { // enter key pressed
				self.checkAnswer($('#answer-input').val());
			}
		});
	},

	loadNextQuestion: function() {
		this.submitAnswerHistory();
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
		this.card = new Card(data);
		console.log(this.card);
		this.state = 'waiting';
	},

	checkAnswer: function(answer) {
		if (this.state == 'correct but first attempt incorrect') 
		{
			this.loadNextQuestion();
			return;
		} 

		this.card.validateAnswer(answer);

		if (this.state == 'waiting' || this.state == 'partial - correct' || this.state == 'partial - incorrect') 
		{
			if (this.card.validation_state == 'correct') 
			{
				this.loadNextQuestion();
			} 
			else if (this.card.validation_state == 'incorrect') 
			{
				this.state = 'incorrect';
			} 
			else if (this.card.validation_state == 'partial - correct') 
			{
				this.state = 'partial - correct';
			} 
			else if (this.card.validation_state == 'partial - incorrect') 
			{
				this.state = 'partial - incorrect';
			}
		} 
		else if (this.state == 'incorrect') 
		{
			if (this.card.validation_state == 'correct') 
			{
				this.state = 'correct but first attempt incorrect';
			}
		} 
		console.log('game.state = ' + this.state);
	},

	submitAnswerHistory: function() {
		if (this.card == undefined) return;

		var body = {
			'session_id': this.session_id,
			'card_id': this.card.card_id,
			'time_to_correct': this.card.time_to_correct,
			'first_attempt_correct': this.card.first_attempt_correct,
		};

		console.log(body);

		$.post('/card/' + this.card.card_id + '/answer', JSON.stringify(body), function(data) { 
			// check for success?
		}, 'json')
		.fail(function(xhr, status, error) {
			console.log('Error submitting answer history: ' + error);
		});
	},

	updateViewForStateWaiting: function () {
		this.card.captureStartTime();
		$('#submit-answer').attr('class', 'btn btn-primary');
		$('#correct-label').fadeOut();
		$('#answer-input').val('');
	}, 

	updateViewForStateFirstAttemptIncorrect: function() {
		$('#incorrect-label').css('display', 'inline');
		$('.question').html(this.card.question); // for multi-part cards that change the CSS
		this.card.resetState();
	},

	updateViewForStateCorrectButFirstAttemptIncorrect: function() {
		$('#incorrect-label').css('display', 'none');
		$('#correct-label').css('display', 'inline');

		$('#submit-answer').text('Next');
		$('#submit-answer').text('Next');
		$('#submit-answer').attr('class', 'btn btn-success');
	},

	updateViewForStatePartial: function () {
		if (this.card.answers == undefined) {
			return;
		}
		
		if (midiInput.onNotes.size == 0 && this.card.validation_states[this.card.current_answer_part_index] == 'unanswered') {
			$('#answer-input').val('');
		}

		for (var i = 0; i < this.card.answers.length; i++) {
			var validation_state = this.card.validation_states[i];
			if (validation_state == "unanswered") {
				break;
			}

			var part = $('.multi-part:eq(' + i + ')');
			part.removeClass('multi-part-unanswered');
			if (validation_state == "incorrect") {
				part.addClass('multi-part-incorrect');
				$('#incorrect-label').css('display', 'inline');
			} else {
				part.removeClass('multi-part-incorrect');
				part.addClass('multi-part-correct');
			}
		}
	}, 
}.init(); };

if (typeof module !== 'undefined' && module.exports) 
	module.exports = Game;

// hook into the webapp
if (typeof window !== 'undefined') {
	window.Game = Game;
}
