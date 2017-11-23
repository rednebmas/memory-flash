var Card = require('./card.js');
var MIDIInput = require('./midi_input.js');
var TextInput = require('./text_input.js');
var FixedQueue = require('./lib/fixed-queue.js');
midiInput = new MIDIInput();
textInput = new TextInput();

// this pattern allows getters and setters (http://stackoverflow.com/a/17606845/337934) and a constructor
// also see the last example from http://stackoverflow.com/a/21648197/337934
var Game = function(session_id, deck_id, user_id) { return { 
	/** 
	Properties 
	**/

	session_id: session_id,
	deck_id: deck_id,
	user_id: user_id,
	input_modality_id: undefined,
	previous_card_ids: new FixedQueue(2),
	// title card, waiting, loading next question, partial - correct, partial - incorrect, incorrect, correct but first attempt incorrect
	_state: 'title card', 
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
			case 'title card':
				this.updateViewForStateTitleCard();
				break;
			case 'waiting':
				this.updateViewForStateWaiting();
				break;
			case 'correct but first attempt incorrect':
				this.updateViewForStateCorrectButFirstAttemptIncorrect();
				break;
			case 'loading next question':
				break;
			case 'partial - correct':
				break;
			case 'partial - incorrect':
				this.updateViewStateForPartialIncorrect();
				break;
			case 'incorrect':
				this.updateViewStateForIncorrect()
				this.showIncorrectLabel();
				break;
			case 'correct':
				this.loadNextQuestion();
				break;
		}
	},

	get card() {
		return this._card;
	},
	set card(card) {
		this._card = card;
		$('#question').html(card.question);
	},

    /**
	Methods
    **/

    init: function () {
		this.bindSubmitAnswer();
		this.setupTitleCard();
		var urlQueryStringParams = new URLSearchParams(window.location.search);
		this.input_modality_id = urlQueryStringParams.get('input_modality_id');
    	return this;
    },

	bindSubmitAnswer: function() {
		var self = this;

		$('#answer-input').focus();
		$("#submit-answer").click(function() {
			self.checkAnswer($('#answer-input').val());
		});
	},

	setupTitleCard: function(arguments) {
		this.updateViewForStateTitleCard();
		$(document).keypress((e) => {
			if (e.which == 99 || e.which == 67) { // c or C
				this.state = 'waiting';
			}
		});
	},

	loadNextQuestion: function() {
		this.submitAnswerHistory();
		if (this.state != 'title card') {
			this.state = 'loading next question';
		}

		if (this.card) {
			this.previous_card_ids.push(this.card.card_id);
		}

		var url = '/session/' + this.session_id + '/next_card';
		var data = { 
			'deck_id' : this.deck_id, 
			'user_id' : this.user_id,
			'previous_card_ids' : this.previous_card_ids
		};

		$.get(url, data, (data) => {
			this.handleCardData(data);
		})
		.fail((xhr, status, error) => {
			console.log('Error retrieving next card: ' + xhr);
			// window.location.href = window.location.origin;
			alert('Error loading next question: ' + error);
		});
	},

	handleCardData: function(data) {
		if ('msg' in data && data['msg'] == 'session complete') {
			if (metronome.isPlaying()) {
				$('#startMetronomeBtn').trigger('click');
			}
			window.location = '/session/' + this.session_id + '/complete'
		}

		if ('session' in data) {
			var tempo = 60.0 / (data['session']['median'] / 4.0) + 5;
			metronome.setTempo(tempo);
			$('#tempoVal').text('' + tempo.toFixed(0));

			var cardsBelowMedianLabel = data.session.cards_below_median + '/' + data.session.total_cards;
			$('#cards-below-median-label').text(cardsBelowMedianLabel);

			$('#metronome-controls').css('display', 'block');
			$('#cards-below-median-label').css('display', 'inline');
		} else {
			$('#metronome-controls').css('display', 'none');
			$('#cards-below-median-label').css('display', 'none');
		}

		this.card = new Card(data);
		var self = this;
		this.card.addEventListener('movedToNextAnswerPart', function(event) {
			$('#incorrect-label').fadeOut();
			$('#correct-label').fadeOut();
			self.clearInput();
		});
		console.log(this.card);

		if (this.state != 'title card') {
			this.state = 'waiting';
		}
	},

	checkAnswer: function(answer) {
		if (this.state == 'correct but first attempt incorrect') 
		{
			this.loadNextQuestion();
			return;
		} 

		this.card.validateAnswer(answer);

		// multipart check answer
		if (this.card.answers != undefined) {
			this.checkAnswerMultiPart(answer);
			return;
		}

		if (this.state == 'waiting')
		{
			if (this.card.validation_state == 'correct') 
			{
				this.state = 'correct';
			}
			else if (this.card.validation_state == 'incorrect')
			{
				this.state = 'incorrect';
			}
		}
		else if (this.state == 'incorrect') 
		{
			if (this.card.validation_state == 'correct') 
			{
				this.state = 'correct but first attempt incorrect';
			}
			else if (this.card.validation_state == 'incorrect')
			{
				this.state = 'incorrect';
			}
		} 
		console.log('game.state = ' + this.state);
	},

	checkAnswerMultiPart: function(answer) {
		// waiting, partial - correct, partial - incorrect
		if (this.state == 'waiting')
		{
			if (this.card.validation_state == 'correct')
			{
				// should never happen unless we have a 1 part multi-part card
				this.state = 'correct';
			}
			else if (this.card.validation_state == 'incorrect')
			{
				// should never happen unless we have a 1 part multi-part card
				this.state = 'waiting';
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
		else if (this.state == 'partial - correct')
		{
			if (this.card.validation_state == 'correct')
			{
				this.state = this.card.first_attempt_correct ? 'correct' : 'correct but first attempt incorrect';
			}
			else if (this.card.validation_state == 'incorrect')
			{
				this.state = 'waiting';
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
		else if (this.state == 'partial - incorrect')
		{
			if (this.card.validation_state == 'correct')
			{
				this.state = 'waiting';
				alert('SHOULD NEVER HAPPEN. Because if we are in partial incorrect, the card should go to incorrect then reset.');
			}
			else if (this.card.validation_state == 'incorrect')
			{
				this.state = 'waiting';
			}
			else if (this.card.validation_state == 'partial - correct')
			{
				this.state = 'partial - correct';
				alert('SHOULD NEVER HAPPEN. Because if we are in partial incorrect, the card should never make to any type of correct state.');
			}
			else if (this.card.validation_state == 'partial - incorrect')
			{
				this.state = 'partial - incorrect';
			}
		}

		console.log('game.state = ' + this.state);
		this.updateMultiPartCorrectnessHighlighting()
	},

	submitAnswerHistory: function() {
		if (this.card == undefined) return;

		var body = {
			'user_id': this.user_id,
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
			alert('Error loading next question: ' + error);
			// window.location.href = window.location.origin;
		});
	},

	updateViewForStateTitleCard: function () {
		$('#question').css('visibility', 'hidden');
	},

	updateViewForStateWaiting: function () {
		this.card.captureStartTime();
		$('#title-card').css('visibility', 'hidden');
		$('#question').css('visibility', 'visible');
		$('#submit-answer').attr('class', 'btn btn-primary');
		$('#correct-label').fadeOut();
		this.clearInput();
	}, 

	showIncorrectLabel: function() {
		$('#incorrect-label').html("Incorrect, the correct answer was: <strong>" + this.card.getAnswer() + "</strong>");
		$('#incorrect-label').css('display', 'inline');
	},

	updateViewForStateCorrectButFirstAttemptIncorrect: function() {
		$('#incorrect-label').css('display', 'none');
		$('#correct-label').css('display', 'inline');

		$('#submit-answer').text('Next');
		$('#submit-answer').text('Next');
		$('#submit-answer').attr('class', 'btn btn-success');
	},

	clearInput: function() {
		if (midiInput.exists()) {
			if (midiInput.onNotes.size != 0) {
				if (this.state == 'waiting' || this.state == 'partial - correct') {
					setTimeout(function() {
						$('#answer-input').val(''); 
					}, 100);
				}
				midiInput.clearOnNotes();
			}
		} else {
			$('#answer-input').val(''); 
		}
	},

	updateViewStateForIncorrect: function() {
		this.clearInput();
	},

	updateViewStateForPartialIncorrect: function () {
		if (midiInput.onNotes.size != 0) {
			midiInput.clearOnNotes();
		}
	},

	updateMultiPartCorrectnessHighlighting: function () {
		if (this.card.answers == undefined) {
			return;
		}

		for (var i = 0; i < this.card.answers.length; i++) {
			var validation_state = this.card.validation_states[i];
			var part = $('.multi-part:eq(' + i + ')');

			part.removeClass('multi-part-incorrect multi-part-correct multi-part-unanswered');
			if (validation_state == "incorrect") {
				part.addClass('multi-part-incorrect');
				this.showIncorrectLabel();
			} else if (['correct', 'correct but first attempt incorrect'].includes(validation_state)) {
				part.addClass('multi-part-correct');
			} else if ('unanswered' == validation_state) {
				part.addClass('multi-part-unanswered');
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
