CREATE TABLE Deck (
	deck_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	descr VARCHAR(500)
);

CREATE INDEX Deck_deck_id_index ON Deck (deck_id);

CREATE TABLE Card (
	card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	deck_id INTEGER NOT NULL, 
	question VARCHAR(2000) NOT NULL,  
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
);

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
);

CREATE INDEX AnswerHistory_card_id_index ON AnswerHistory (card_id);
CREATE INDEX AnswerHistory_session_id_index ON AnswerHistory (session_id);
CREATE INDEX AnswerHistory_answered_at_index ON AnswerHistory (answered_at);
CREATE INDEX AnswerHistory_answered_at_index_day ON AnswerHistory (answered_at_day);

CREATE TABLE SessionCard (
	session_card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	session_id INTEGER NOT NULL,
	card_id INTEGER NOT NULL
);

CREATE INDEX SessionCard_card_id_index ON SessionCard (card_id);
CREATE INDEX SessionCard_id_index ON SessionCard (session_id);

CREATE TABLE Migration (
	migration_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	migrations_performed INTEGER
);

INSERT INTO Migration (migrations_performed) VALUES (0);
