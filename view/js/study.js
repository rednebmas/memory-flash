// possible: correct, waiting_for_correct
var state = "waiting_for_correct";
var card = {};

function checkAnswer() {
    var userAnswer = $('#answer-input').val();

    if (state == "correct") {
        loadNextQuestion();
    } else if (answer_validator(userAnswer, card.answer)) {
        card.time_to_correct = (performance.now() - card.start_time) / 1000.0;
        console.log('Time to correct: ' + card.time_to_correct);
        submitAnswerHistory(card);

        $('#incorrect-label').css('display', 'none');
        $('#correct-label').css('display', 'inline');

        if (state == "first_attempt_incorrect") {
        	state = "correct";
			$('#submit-answer').text('Next');
			$('#submit-answer').attr('class', 'btn btn-success');
        } else {
        	loadNextQuestion();
        }
    } else if (state == "waiting_for_correct") {
    	markIncorrect();
    }
}

function markIncorrect() {
    console.log('marked incorrect');
	state = "first_attempt_incorrect";
	card.first_attempt_correct = false;
	$('#incorrect-label').css('display', 'inline');
	$('#correct-label').css('display', 'none');
}

function loadNextQuestion() {
	state = "loading_next_question";
	$('#submit-answer').text('Submit');
	$('#answer-input').val('');

    $.post('/session/'+session_id+'/next_card', JSON.stringify({ 'deck_id' : deck_id }), function (data) {
        console.log(data);
        $('.question').html(data['question']);
        card = data;
        card.start_time = performance.now();
        card.first_attempt_correct = true;
        state = "waiting_for_correct";
        $('#submit-answer').attr('class', 'btn btn-primary');
        $('#correct-label').fadeOut();
    }, 'json')
    .fail(function(xhr, status, error) {
        console.log('Error retrieving next card');
        console.log(xhr);
    });
}

function submitAnswerHistory(card) {
    var body = JSON.stringify({
        'session_id': session_id,
        'card_id': card.card_id,
        'time_to_correct': card.time_to_correct,
        'first_attempt_correct': card.first_attempt_correct,
    });
    $.post('/card/'+card.card_id+'/answer', body, function (data){ 
        // check for success?
    }, 'json')
    .fail(function(xhr, status, error) {
        // error handling
        console.log(xhr);
    });
}

$(document).ready(function() {
    loadNextQuestion();

    $('#answer-input').focus();
	$("#submit-answer").click(function() {
		checkAnswer();
	});

	$('#answer-input').keypress(function(e) {
		if (e.which == 13) { // enter key pressed
			checkAnswer();
		}
	});
});
