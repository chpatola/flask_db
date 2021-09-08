--- TABLE CREATIONS
CREATE TABLE IF NOT EXISTS userstest (
	username VARCHAR (50) PRIMARY KEY,
	password VARCHAR (50) NOT NULL,
   firstname VARCHAR (100) NOT NULL,
   lastname VARCHAR (100) NOT NULL,
   phone VARCHAR (100) NOT NULL,
   bornyear INTEGER,
   usertype VARCHAR (15) NOT NULL,
   removed BOOLEAN NOT NULL

);

CREATE TABLE IF NOT EXISTS teacherstest (
	id SERIAL PRIMARY KEY,
   firstname VARCHAR (100) NOT NULL,
   lastname VARCHAR (100) NOT NULL,
   phone VARCHAR (100),
   email VARCHAR (100) UNIQUE NOT NULL,
   hourlysalary FLOAT
);

CREATE TABLE IF NOT EXISTS roomstest (
	id SERIAL PRIMARY KEY,
   m2 FLOAT,
   capacity INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS coursestest (
	id SERIAL PRIMARY KEY,
   name VARCHAR(200) NOT NULL,
   startdate DATE,
   enddate DATE,
   time TIME,
   durationhour FLOAT,
   occurances INTEGER,
   teacher_id INTEGER REFERENCES teacherstest,
   room_id INTEGER REFERENCES roomstest

);

CREATE TABLE IF NOT EXISTS courseenrolmentstest (
	id SERIAL PRIMARY KEY,
   course_id INTEGER REFERENCES coursestest,
   user_id VARCHAR(50) REFERENCES userstest ON DELETE SET NULL,
   UNIQUE (course_id, user_id)

);
--- INSERTS

INSERT INTO userstest VALUES (
   'immi@hei.com',
   'testpassword',
   'Immi',
   'Heinonen',
   '0504217550',
   1997,
   'student',
   FALSE

) ON CONFLICT (username) DO NOTHING;

INSERT INTO teacherstest (firstname,lastname, phone, email,hourlysalary) VALUES (
   'John',
   'Travolta',
   '0421782',
   'johnnie@aida.com',
   60.50

) ON CONFLICT (email) DO NOTHING;

INSERT INTO roomstest (m2, capacity) VALUES (
   20.5,
   8

);

INSERT INTO coursestest (name,startdate, enddate, time, durationhour, occurances, teacher_id, room_id) VALUES (
   'First Steps Class - Girls aged 8 - 10',
   '2022-01-09',
   '2022-04-10',
   '16:00',
   1,
   16,
   1,
   1
);

INSERT INTO courseenrolmentstest (course_id, user_id) VALUES (
   1,
   'immi@hei.com'
) ON CONFLICT (course_id, user_id) DO NOTHING;

