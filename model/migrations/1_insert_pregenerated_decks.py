import random
from model.card_generators.times_table_generator import TimesTableGenerator
from model.card_generators.notes_generator import NotesGenerator
from model.card_generators.intervals_generator import IntervalsGenerator
from model.card_generators.chords_generator import ChordsGenerator
from model.card_generators.progression_generator import ProgressionGenerator
from model.card_generators.scale_generator import ScaleGenerator

def insert_deck(db, deck_name, deck_desc, cards):
	db.execute(
		""" INSERT INTO Deck (name, descr) VALUES (?, ?)""",
		(deck_name, deck_desc)
	)
	deck_id = db.select1(table="Deck", where="name = ?", substitutions=(deck_name,))['deck_id']
	for c in cards: c['deck_id'] = deck_id
	db.insert_key_value_pairs('Card', cards)

insert_deck(
	db, 
	"Intervals", 
	"Interval math!", 
	IntervalsGenerator.generate_cards()
)

insert_deck(
	db, 
	'Major Triads', 
	'Major triads in all inversions', 
	ChordsGenerator.generate_major_chord_cards()
)

insert_deck(
	db, 
	'Minor Triads', 
	'Minor triads in all inversions', 
	ChordsGenerator.generate_minor_chord_cards()
)

insert_deck(
	db, 
	'Diminished Triads', 
	'Diminished triads in all inversions', 
	ChordsGenerator.generate_dim_chords_cards()
)

insert_deck(
	db, 
	'Augmented Triads', 
	'Augmented triads in all inversions', 
	ChordsGenerator.generate_aug_chords_cards()
)

insert_deck(
	db, 
	'Major and Minor Chords', 
	'Major and Minor triads in all inversions', 
	ChordsGenerator.generate_major_and_minor_chord_cards()
)

triads = ChordsGenerator.generate_major_and_minor_chord_cards() + \
         ChordsGenerator.generate_aug_chords_cards() + \
         ChordsGenerator.generate_dim_chords_cards()
random.shuffle(triads)
insert_deck(
	db, 
	'All triads', 
	'All triads in all inversions', 
	triads
)

insert_deck(
	db, 
	'I V vi IV w/ chord symbols', 
	'The four chord song progression', 
	ProgressionGenerator.one_five_six_four_cards()
)

insert_deck(
	db, 
	'IV V I', 
	'Includes common sets of inversions', 
	ProgressionGenerator.four_five_one_cards()
)

insert_deck(
	db, 
	'ii V I', 
	'Root, Thirds, and Sevenths', 
	ProgressionGenerator.two_7_five_7_one_M7__root_three_seven__cards()
)

insert_deck(
	db, 
	'Natural Minor Scales', 
	'All of \'em', 
	ScaleGenerator.natural_minor()
)

insert_deck(
	db, 
	'Harmonic Minor Scales', 
	'All of \'em', 
	ScaleGenerator.harmonic_minor()
)

insert_deck(
	db, 
	'Meldoic Minor Scales', 
	'All of \'em', 
	ScaleGenerator.melodic_minor()
)

all_minor = ScaleGenerator.melodic_minor() + \
            ScaleGenerator.harmonic_minor() + \
            ScaleGenerator.natural_minor()
random.shuffle(all_minor)
insert_deck(
	db, 
	'All Minor Scales', 
	'All of \'em. Natural, Harmonic, and Melodic!', 
	all_minor
)

insert_deck(
	db, 
	'The Blues', 
	'All of \'em.', 
	ScaleGenerator.blues()
)

