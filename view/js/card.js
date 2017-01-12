function Card(json) {
	this.question = json['question'];
	this.answers = json['answer'].split('|');
	this.deck_id = json['deck_id'];
	this.card_id = json['card_id'];
	if ('accidental_type' in json) {
		this.accidental_type = json['accidental_type'];
	}
}

if (typeof exports !== 'undefined') 
	exports.Card = Card;