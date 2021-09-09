--- TABLE CREATIONS
CREATE TABLE IF NOT EXISTS userstest (
   username VARCHAR (50) PRIMARY KEY,
   password VARCHAR (200) NOT NULL,
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
   name VARCHAR (50) UNIQUE NOT NULL,
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
   room_id INTEGER REFERENCES roomstest,
   UNIQUE (name, startdate, enddate, time, room_id)
);
CREATE TABLE IF NOT EXISTS courseenrolmentstest (
   id SERIAL PRIMARY KEY,
   course_id INTEGER REFERENCES coursestest,
   user_id VARCHAR(50) REFERENCES userstest ON DELETE SET NULL,
   UNIQUE (course_id, user_id)
);
--- INSERTS
INSERT INTO userstest
VALUES (
      'immi@hei.com',
      'testpassword',
      'Immi',
      'Heinonen',
      '0504217550',
      1997,
      'student',
      FALSE
   ),
   (
      'erik@heida.com',
      'pbkdf2:sha256:150000$M70SLHTh$1e3de775805c644919b6179fc79fef23fb746c62c89b8d0339651191993dfe46',
      'Erik',
      'Gran',
      '0457819',
      2014,
      'student',
      FALSE
   )
    ON CONFLICT (username) DO NOTHING;

INSERT INTO teacherstest (firstname, lastname, phone, email, hourlysalary)
VALUES (
      'John',
      'Travolta',
      '0421782',
      'johnnie@aida.com',
      60.50
   ),
   (
      'Olivia',
      'Newton-John',
      '0421782',
      'olivia@aida.com',
      60.90
   ) ON CONFLICT (email) DO NOTHING;

INSERT INTO roomstest (name, m2, capacity)
VALUES ('Room 1', 20.5, 8), ('Room 2', 30 ,12) ON CONFLICT (name) DO NOTHING;


INSERT INTO coursestest (
      name,
      startdate,
      enddate,
      time,
      durationhour,
      occurances,
      teacher_id,
      room_id
   )
VALUES (
      'First Steps Class - Girls aged 8 - 10',
      '2022-01-09',
      '2022-04-10',
      '16:00',
      1,
      16,
      1,
      1
   ),
   (
      'First Steps Class - Boys aged 8 - 10',
      '2022-01-09',
      '2022-04-10',
      '16:00',
      1,
      16,
      1,
      2
   ),
   (
      'Advanced Steps',
      '2021-01-09',
      '2021-06-10',
      '18:00',
      2,
      22,
      17,
      2
   ) ON CONFLICT (name, startdate, enddate, time, room_id) DO NOTHING;
INSERT INTO courseenrolmentstest (course_id, user_id)
VALUES (3, 'immi@hei.com'), (4, 'erik@heida.com') ON CONFLICT (course_id, user_id) DO NOTHING;


