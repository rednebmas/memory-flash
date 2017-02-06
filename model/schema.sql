CREATE TABLE Deck (
	deck_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	descr VARCHAR(500)
);

CREATE TABLE Card (
	card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	deck_id INTEGER NOT NULL, 
	question VARCHAR(2000) NOT NULL,  
	answer VARCHAR(2000) NOT NULL,
	answer_validator VARCHAR(256)
);

CREATE TABLE Session (
	session_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	deck_id INTEGER NOT NULL, 
	begin_date DATETIME NOT NULL, 
	end_date DATETIME,
	median DOUBLE,
	stage varchar(25) DEFAULT 'aquire'
);

CREATE TABLE AnswerHistory (
	answer_history_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	session_id INTEGER NOT NULL, 
	card_id INTEGER NOT NULL, 
	time_to_correct DOUBLE NOT NULL, 
	first_attempt_correct BOOLEAN NOT NULL, 
	answered_at DATETIME NOT NULL,
	answered_at_day DATE NOT NULL
);

CREATE TABLE SessionCard (
	session_card_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
	session_id INTEGER NOT NULL,
	card_id INTEGER NOT NULL
);

CREATE TABLE Migration (
	migration_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	migrations_performed INTEGER
);

INSERT INTO Migration (migrations_performed) VALUES (0);
