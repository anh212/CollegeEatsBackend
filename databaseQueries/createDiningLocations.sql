DROP TABLE dining_locations CASCADE;


CREATE TABLE dining_locations (
	school_id smallint NOT NULL references schools(school_id),
	dining_id smallserial PRIMARY KEY,
	dining_name varchar(100) NOT NULL,
	location_name varchar(100) NOT NULL
)