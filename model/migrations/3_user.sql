CREATE TABLE User (
	user_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	email varchar(256),
	user_name VARCHAR(256) NOT NULL,
	password VARCHAR(256) NOT NULL
);

CREATE INDEX User_user_name_index ON User (user_id);

ALTER TABLE Session ADD COLUMN user_id INTEGER;
CREATE INDEX Session_user_id_index ON Session (user_id);

ALTER TABLE SessionCard ADD COLUMN user_id INTEGER;
CREATE INDEX SessionCard_user_id_index ON SessionCard (user_id);

ALTER TABLE AnswerHistory ADD COLUMN user_id INTEGER;
CREATE INDEX AnswerHistory_user_id_index ON AnswerHistory (user_id);
