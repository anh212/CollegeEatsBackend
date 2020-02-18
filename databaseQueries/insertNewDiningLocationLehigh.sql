INSERT INTO dining_locations (school_id, dining_name, location_name) VALUES (
	(SELECT school_id FROM schools WHERE school_name='lehigh'),
	'Lower Cort',
	'Lower University Center'
)