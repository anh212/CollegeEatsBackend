INSERT INTO hours (school_id, dining_id, daynum, starttime, endtime) VALUES (
	(SELECT school_id FROM schools WHERE school_name='lehigh'),
	(SELECT dining_id FROM dining_locations WHERE dining_name='Lower Cort'),
	1,
	7,
	19
)