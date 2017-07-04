with open('model/migrations/4_input_modality.sql') as f:
	db.execute_statments(f.read().split(';'))
