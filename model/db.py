import sqlite3
import time    
import sys
import os.path
from model.migration_manager import MigrationManager

class DB:
	def __init__(self, path):
		self.path = path
		self.conn = sqlite3.connect(path)
		self.conn.row_factory = sqlite3.Row
		self.cursor = self.conn.cursor()

	def __del__(self):
		self.conn.close()

	def close_conn(self):
		self.conn.close()

	def execute(self, statement, substitutions=(), debug=False):
		if debug: print(DB.put_substitutions_in_statement(statement, substitutions))
		self.cursor.execute(statement, substitutions)
		self.conn.commit()

	def execute_statments(self, statements, debug=False):
		""" :param statements
			an array of sql statements
		"""
		for statement in statements:
			if debug: print(statement)
			self.cursor.execute(statement)
		self.conn.commit()

	def select(self, table, substitutions=(), columns="*", where="", order_by="", limit="", debug=False):
		if where: where = "WHERE " + where
		if order_by: order_by = "ORDER BY " + order_by
		if limit: limit = "LIMIT " + limit

		statement = "SELECT {} FROM {} {} {} {}".format(columns, table, where, order_by, limit)
		if debug: print(DB.put_substitutions_in_statement(statement, substitutions))

		self.cursor.execute(statement, substitutions)
		rows = self.cursor.fetchall()

		if debug: print(rows)
		return rows

	def select1(self, table, where, substitutions=(), columns="*", order_by="", debug=False):
		# ABSTRACT THIS TO SELECT
		rows = self.select(
			table=table, 
			where=where,
			substitutions=substitutions, 
			columns=columns, 
			order_by=order_by, 
			limit="1",
			debug=debug
		)

		if len(rows) < 1: return None
		else: return rows[0]

	def insert_key_value_pairs(self, table, data):
		"""Inserts array of dictionaries into database
		@data:
			format should be as follows: [{"row" : "value"}]

		!IMPORTANT! At the moment this is not safe to use for data recieved from the internet as it is susceptible to SQL injection
		"""
		statements = []
		for d in data:
			column_string = ','.join(d.keys())
			values = ['"'+v.replace('"', '""')+'"' if isinstance(v, str) else str(v) for v in d.values()]
			value_string = ','.join(values)
			statements.append("""INSERT INTO {} ({}) VALUES ({})""".format(table, column_string, value_string))
		self.execute_statments(statements)

	def unittest_reset(self):
		self.conn.close()
		self.conn = sqlite3.connect(':memory:')
		self.conn.row_factory = sqlite3.Row
		self.cursor = self.conn.cursor()
		MigrationManager.create_db(self)
		MigrationManager.run_pending_migrations(self)

	@staticmethod
	def put_substitutions_in_statement(statement, substitutions):
		subbed = statement
		for sub in substitutions:
			if isinstance(sub, str) is False: sub = str(sub) 
			subbed = subbed.replace('?', sub, 1)
		return subbed

	@staticmethod
	def datetime_now():
		return time.strftime('%Y-%m-%d %H:%M:%S')

if 'unittest' in sys.argv[0]:
	db = DB(':memory:')
	MigrationManager.create_db(db)
else:
	db_path = 'memory-flash.db'
	db_exists = os.path.isfile(db_path)
	db = DB(db_path)
	if db_exists is False:
		print('Creating database')
		MigrationManager.create_db(db)

MigrationManager.run_pending_migrations(db)

