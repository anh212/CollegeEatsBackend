DROP TABLE hours CASCADE;

CREATE TABLE hours (
	time_id serial PRIMARY KEY,
	school_id smallint NOT NULL references schools(school_id),
	dining_id smallint NOT NULL references dining_locations(dining_id),
	dayNum smallint NOT NULL,
	startTime decimal NOT NULL,
	endTime decimal NOT NULL
)
