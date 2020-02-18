DROP TABLE schools CASCADE;


CREATE TABLE schools (
	school_id SMALLSERIAL PRIMARY KEY,
	school_name varchar(100) NOT NULL
);