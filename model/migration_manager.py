import sys
import os.path
import re
import importlib.util
from glob import glob
from model.card_generators.times_table_generator import TimesTableGenerator
from model.card_generators.notes_generator import NotesGenerator
from model.card_generators.intervals_generator import IntervalsGenerator
from model.card_generators.chords_generator import ChordsGenerator
from model.card_generators.progression_generator import ProgressionGenerator

class MigrationManager:
	@staticmethod
	def create_db(db):
		with open('model/migrations/initial_schema.sql') as f:
			db.execute_statments(f.read().split(';'))

	@staticmethod
	def run_pending_migrations(db):
		migrations_performed = db.select1(table="Migration", where="migration_id = 1")['migrations_performed']
		print("run pending:",  migrations_performed)

		num_migrations_updated = False
		for filename in sorted(glob('model/migrations/*.py')):
			migration_int = int( re.search(r'model/migrations/(\d).*\.py', filename).group(1) )
			if migrations_performed < migration_int:
				# execute file
				with open(filename) as f:
					code = compile(f.read(), filename, 'exec')
					exec(code) 
				# assure it was executed
				print('Performed migration: ' + filename.replace('model/migrations/', ''))
				# let us know that we should update the migration table
				num_migrations_updated = True

		if num_migrations_updated:
			db.execute("UPDATE Migration SET migrations_performed = ? WHERE migration_id = 1", (migration_int,))
