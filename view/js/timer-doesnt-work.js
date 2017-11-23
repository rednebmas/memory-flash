var alreadySetColorToGreen = false;
function endOfDay() {
	var end = new Date();
	end.setHours(23,59,59,999);
	return end;
}

// display elapsed time in the lower right
// should definitely store this data in a cookie...
// as well as whether the metronome is on
function startTimer() {
	var secondsElapsed = Cookies.get('secondsElapsed');
	if (secondsElapsed == undefined) {
		secondsElapsed = 0;
		Cookies.set('secondsElapsed', 0, { expires: endOfDay() });
	} else {
		// convert to integer
		secondsElapsed = +secondsElapsed;
	}

	if (secondsElapsed > 60 && !alreadySetColorToGreen) {
		$('#timer').css('color', 'green');
		alreadySetColorToGreen = true;
	}

	var seconds = secondsElapsed %  60;
	var minutes = Math.floor(secondsElapsed /  60);
	var hours = Math.floor(secondsElapsed / 60 / 60);

	var time = pad(minutes) + ":" + pad(seconds);
	if (hours > 1) {
		time = hours + ":" + time
	}

	document.getElementById('timer').innerHTML = time;

	secondsElapsed += 1;
	Cookies.set('secondsElapsed', secondsElapsed);

	var t = setTimeout(function() { startTimer(); }, 1000);
}
function pad(i) {
	if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
	return i;
}

$(document).ready(function () {
	// startTimer();
})  