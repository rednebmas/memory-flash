from model.db import db
from model.exceptions import ValidationError

def exists(property_dict):
	import inspect
	import os.path

	# this was being used for instances
	# cls_name = inspect.stack()[1][0].f_locals["self"].__class__.__name__
    # table = ''.join(map(lambda s: s.title(), cls_name.split('_')))

    # gets table name from filename
	caller_file_path = inspect.currentframe().f_back.f_code.co_filename
	caller_file_name = os.path.splitext(os.path.basename(caller_file_path))[0]
	table = ''.join(map(lambda s: s.title(), caller_file_name.split('_')))

	error_columns = []
	for key, value in property_dict.items():
		where_clause = key + " = ?"
		num = len( db.select(table=table, where=where_clause, substitutions=(value,)) )
		if num == 0:
			error_columns.append(key)

	if len(error_columns):
		return error_columns
	else: 
		return True
