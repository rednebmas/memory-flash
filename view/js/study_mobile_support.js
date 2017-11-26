(function() {
	var supportsTouch = 'ontouchstart' in window || navigator.msMaxTouchPoints;
	if (!supportsTouch) return;

	$('#press-any-key-to-continue').text('Tap anywhere to begin');
	$('#title-card').on({
		'touchstart': () => {
			game.state = 'waiting';
		}
	});
}());


