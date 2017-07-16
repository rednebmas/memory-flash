--
-- InputModality
--
CREATE TABLE InputModality (
	input_modality_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	input_modality_name VARCHAR(512) NOT NULL
);

INSERT INTO InputModality (input_modality_name) VALUES ('Text'), ('MIDI Left Hand'), ('MIDI Right Hand'), ('MIDI Both Hands');

--
-- DeckInputModality
--
CREATE TABLE DeckInputModality (
	deck_input_modality_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	input_modality_id INTEGER NOT NULL,
	deck_id INTEGER NOT NULL
);

CREATE INDEX DeckInputModality_deck_id_input_modality_id_index ON DeckInputModality (deck_id, input_modality_id);
CREATE INDEX DeckInputModality_deck_id_index ON DeckInputModality (deck_id);

-- ii V I: Root, Thirds, and Sevenths
-- Text and both hands
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 9), (4, 9);

-- Scales
-- Text, left hand, right hand, both hands
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 10), (2, 10), (3, 10), (4, 10);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 11), (2, 11), (3, 11), (4, 11);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 12), (2, 12), (3, 12), (4, 12);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 13), (2, 13), (3, 13), (4, 13);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 14), (2, 14), (3, 14), (4, 14);

INSERT INTO InputModality (input_modality_name) VALUES ('Text'), ('MIDI Left Hand'), ('MIDI Right Hand'), ('MIDI Both Hands');
-- Everything else
-- Text, left hand, right hand
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 1), (2, 1), (3, 1);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 2), (2, 2), (3, 2);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 3), (2, 3), (3, 3);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 4), (2, 4), (3, 4);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 5), (2, 5), (3, 5);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 6), (2, 6), (3, 6);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 7), (2, 7), (3, 7);
INSERT INTO DeckInputModality (input_modality_id, deck_id) VALUES (1, 8), (2, 8), (3, 8);

--
-- Session
--
ALTER TABLE Session ADD COLUMN input_modality_id INTEGER;
UPDATE Session SET input_modality_id = 2 WHERE deck_id <> 9;
UPDATE Session SET input_modality_id = 4 WHERE deck_id = 9;
CREATE INDEX Session_input_modality_id_index ON Session (input_modality_id);

--
-- Bug
-- 
DELETE FROM Card WHERE deck_id = 1 AND (answer LIKE '_##' OR answer LIKE '_bb');