-- $ sqlite3 memory-flash.db .schema
CREATE TABLE Deck (
	deck_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	descr VARCHAR(500)
);
CREATE INDEX Deck_deck_id_index ON Deck (deck_id);

CREATE TABLE Card (
	card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	deck_id INTEGER NOT NULL, 
	template_path VARCHAR(2000) NOT NULL, 
	template_data VARCHAR(2000) NOT NULL, 
	answer VARCHAR(2000) NOT NULL,
	answer_validator VARCHAR(256),
	accidental CHAR(1),
	scale VARCHAR(32)
);
CREATE INDEX Card_card_id_index ON Card (card_id);
CREATE INDEX Card_deck_id_index ON Card (deck_id);

CREATE TABLE Session (
	session_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	deck_id INTEGER NOT NULL, 
	begin_date DATETIME NOT NULL, 
	end_date DATETIME,
	median DOUBLE,
	stage varchar(25) DEFAULT 'aquire'
, user_id INTEGER, input_modality_id INTEGER);
CREATE INDEX Session_session_id_index ON Session (session_id);
CREATE INDEX Session_deck_id_index ON Session (deck_id);

CREATE TABLE AnswerHistory (
	answer_history_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	session_id INTEGER NOT NULL, 
	card_id INTEGER NOT NULL, 
	time_to_correct DOUBLE NOT NULL, 
	first_attempt_correct BOOLEAN NOT NULL, 
	answered_at DATETIME NOT NULL,
	answered_at_day DATE NOT NULL
, user_id INTEGER);
CREATE INDEX AnswerHistory_card_id_index ON AnswerHistory (card_id);
CREATE INDEX AnswerHistory_session_id_index ON AnswerHistory (session_id);
CREATE INDEX AnswerHistory_answered_at_index ON AnswerHistory (answered_at);
CREATE INDEX AnswerHistory_answered_at_index_day ON AnswerHistory (answered_at_day);

CREATE TABLE SessionCard (
	session_card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	session_id INTEGER NOT NULL,
	card_id INTEGER NOT NULL
, user_id INTEGER);
CREATE INDEX SessionCard_card_id_index ON SessionCard (card_id);
CREATE INDEX SessionCard_id_index ON SessionCard (session_id);

CREATE TABLE Migration (
	migration_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	migrations_performed INTEGER
);

CREATE TABLE User (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	user_name VARCHAR(256) NOT NULL,
	password VARCHAR(256) NOT NULL
, email varchar(256));
CREATE INDEX User_user_name_index ON User (user_id);
CREATE INDEX Session_user_id_index ON Session (user_id);
CREATE INDEX SessionCard_user_id_index ON SessionCard (user_id);
CREATE INDEX AnswerHistory_user_id_index ON AnswerHistory (user_id);

CREATE TABLE InputModality (
	input_modality_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	input_modality_name VARCHAR(512) NOT NULL
);

CREATE TABLE DeckInputModality (
	deck_input_modality_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	input_modality_id INTEGER NOT NULL,
	deck_id INTEGER NOT NULL
);
CREATE INDEX DeckInputModality_deck_id_input_modality_id_index ON DeckInputModality (deck_id, input_modality_id);
CREATE INDEX Session_input_modality_id_index ON Session (input_modality_id);