var TextInput = function() { return { 
    previousInput: undefined,

    init: function() {
        var self = this;
		$('#answer-input').keypress(function(e) {
            var returnVal = true;

            switch (e.which) {
                case 115:
                    this.value = this.value + "#";
                    returnVal = false;
                    break;
                case 97:
                    this.value = this.value + "A";
                    returnVal = false;
                    break;
                case 98:
                    this.value = this.value + "B";
                    returnVal = false;
                    break;
                case 99:
                    this.value = this.value + "C";
                    returnVal = false;
                    break;
                case 100:
                    this.value = this.value + "D";
                    returnVal = false;
                    break;
                case 101:
                    this.value = this.value + "E";
                    returnVal = false;
                    break;
                case 102:
                    this.value = this.value + "F";
                    returnVal = false;
                    break;
                case 103:
                    this.value = this.value + "G";
                    returnVal = false;
                    break;
                case 13:
                    game.checkAnswer($('#answer-input').val());
                    break;
                default:
                    break;
            }

            this.value = this.value.replace("S", "#");
            this.value = this.value.replace(/([A-G])BB/g, "$1bb");
            this.value = this.value.replace(/([A-G])B/g, "$1b");

            this.previousInput = e.which;
            return returnVal;

		});
    }
}.init() };

if (typeof module !== 'undefined' && module.exports) 
	module.exports = TextInput;