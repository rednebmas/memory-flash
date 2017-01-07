// possible: correct, waiting_for_correct
var state = "waiting_for_correct";

function checkAnswer() {
    var userAnswer = $('#answer-input').val();
    if (state == "correct") {
        loadNextQuestion();
        state = "loading_next_question";
        $('#submit-answer').text('Submit');
    } else if (answer_validator(userAnswer, card.answer)) {
        card.time_to_correct = (performance.now() - card.start_time) / 1000.0;
        console.log('Time to correct: ' + card.time_to_correct);
        submitAnswerHistory(card);
        $('#incorrect-label').css('display', 'none');
        $('#correct-label').css('display', 'inline');
        $('#answer-input').val('');
        state = "correct";
        $('#submit-answer').text('Next');
        $('#submit-answer').attr('class', 'btn btn-success');
    } else if (state == "waiting_for_correct") {
        card.first_attempt_correct = false;
        $('#incorrect-label').css('display', 'inline');
        $('#correct-label').css('display', 'none');
    }
}

function loadNextQuestion() {
    $.post('/decks/'+card.deck_id+'/next_card', JSON.stringify({ 'session_id' : session_id }), function (data) {
        $('.question').html(data['question']);
        card = data;
        card.start_time = performance.now();
        card.first_attempt_correct = true;
        state = "waiting_for_correct";
        $('#submit-answer').attr('class', 'btn btn-primary');
        $('#correct-label').fadeOut();
    }, 'json');
}

function submitAnswerHistory(card) {
    var body = JSON.stringify({
        'session_id': session_id,
        'card_id': card.card_id,
        'time_to_correct': card.time_to_correct,
        'first_attempt_correct': card.first_attempt_correct,
    });
    console.log(body);
    $.post('/card/'+card.card_id+'/answer', body, function (data){ 
        // check for success?
    }, 'json')
    .fail(function(xhr, status, error) {
        // error handling
        console.log(xhr);
    });
}

$("#submit-answer").click(function() {
    checkAnswer();
});

$('#answer-input').keypress(function(e){
    if (e.which == 13) { // enter key pressed
        checkAnswer();
    }
});

$(document).ready(function() {
    $('#answer-input').focus();
    loadNextQuestion();
});

/*
$("input[type=text], textarea").mouseover(zoomDisable).mousedown(zoomEnable);
function zoomDisable(){
  $('head meta[name=viewport]').remove();
  $('head').prepend('<meta name="viewport" content="user-scalable=0" />');
}
function zoomEnable(){
  $('head meta[name=viewport]').remove();
  $('head').prepend('<meta name="viewport" content="user-scalable=1" />');
} */
