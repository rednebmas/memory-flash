with open('model/migrations/3_user.sql') as f:
	db.execute_statments(f.read().split(';'))
