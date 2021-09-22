--- TABLE CREATIONS
CREATE TABLE IF NOT EXISTS users (
   username VARCHAR (50) PRIMARY KEY,
   password VARCHAR (200) NOT NULL,
   firstname VARCHAR (100) NOT NULL,
   lastname VARCHAR (100) NOT NULL,
   phone VARCHAR (100) NOT NULL,
   bornyear INTEGER,
   usertype VARCHAR (15) NOT NULL,
   removed BOOLEAN NOT NULL
);
CREATE TABLE IF NOT EXISTS teachers (
   id SERIAL PRIMARY KEY,
   firstname VARCHAR (100) NOT NULL,
   lastname VARCHAR (100) NOT NULL,
   phone VARCHAR (100),
   email VARCHAR (100) UNIQUE NOT NULL,
   hourlysalary FLOAT
);
CREATE TABLE IF NOT EXISTS rooms (
   id SERIAL PRIMARY KEY,
   name VARCHAR (50) UNIQUE NOT NULL,
   m2 FLOAT,
   capacity INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS courses (
   id SERIAL PRIMARY KEY,
   name VARCHAR(200) NOT NULL,
   startdate DATE NOT NULL,
   enddate DATE NOT NULL,
   time TIME NOT NULL,
   durationhour FLOAT NOT NULL,
   occurances INTEGER NOT NULL,
   teacher_id INTEGER REFERENCES teachers,
   room_id INTEGER REFERENCES rooms,
   price FLOAT NOT NULL,
   UNIQUE (name, startdate, enddate, time, room_id)
);
CREATE TABLE IF NOT EXISTS courseenrolments (
   id SERIAL PRIMARY KEY,
   course_id INTEGER REFERENCES courses,
   user_id VARCHAR(50) REFERENCES users ON DELETE SET NULL,
   UNIQUE (course_id, user_id)
);
--- INSERTS
INSERT INTO users
VALUES (
      'info@aidadanceschool.com',
      'pbkdf2:sha256:150000$1RTNARr3$2b28e981f26382a7c33e47f6d05603d7591a90feb85b449255e2e209c78a5216',--- aidarocks_
      'Admin',
      'Admin',
      '048 456 234 08 ',
      1995,
      'admin',
      FALSE
   ),
   (
      'student12@student.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', --- <3aidadance
      'Steven',
      'Student',
      '0907810253',
      2000,
      'student',
      FALSE
   ),
   (
      'immi@hei.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a',
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
   ),
   (
      'enna@heida.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Enna',
      'Gran',
      '0457817',
      2015,
      'student',
      FALSE
   ),
   (
      'ennalisa@heida.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Ennalisa',
      'Granlund',
      '0457818',
      2013,
      'student',
      FALSE
   ),
   (
      'mimmi@cool.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Mimmi',
      'Pigg',
      '0407818',
      2015,
      'student',
      FALSE
   ),
   (
      'anders@cool.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a',
      'Anders',
      'Pigg',
      '0407818',
      2015,
      'student',
      FALSE
   ),
   (
      'anders-erik@cool.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Anders',
      'Eriksson',
      '0407818 015',
      2014,
      'student',
      FALSE
   ),
   (
      'eve@hot.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Eve',
      'Eriksson',
      '0407818 015',
      2014,
      'student',
      FALSE
   ),
   (
      'maria@hot.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'maria',
      'Eriksson',
      '05047819',
      2012,
      'student',
      FALSE
   ),
   (
      'calle@calle.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a',
      'Calle',
      'Calleson',
      '05846145',
      2012,
      'student',
      FALSE
   ),
   (
      'carla@calle.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Carla',
      'Calleson',
      '045 7864542',
      2013,
      'student',
      FALSE
   ),
   (
      'carlise@calle.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Carlise',
      'Calleson',
      '045 78645428',
      2014,
      'student',
      FALSE
   ),
   (
      'gwyn@hi.com',
      'pbkdf2:sha256:150000$cjCV8Tq7$c66999c9a288528d38a1ce04c1e334bfd14b70ab33b9c4d5edeb492bd19f058a', 
      'Gwyn',
      'Devin',
      '045 7454352',
      2015,
      'student',
      FALSE
   )
   
   
   
  
    ON CONFLICT (username) DO NOTHING;

INSERT INTO teachers (firstname, lastname, phone, email, hourlysalary)
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

INSERT INTO rooms (name, m2, capacity)
VALUES ('Room 1', 20.5, 8), ('Room 2', 30 ,12) ON CONFLICT (name) DO NOTHING;


INSERT INTO courses (
      name,
      startdate,
      enddate,
      time,
      durationhour,
      occurances,
      teacher_id,
      room_id,
      price
   )
VALUES (
      'First Steps Class - Girls aged 8 - 10',
      '2022-01-09',
      '2022-04-10',
      '16:00',
      1,
      16,
      1,
      1,
      256
   ),
   (
      'First Steps Class - Boys aged 8 - 10',
      '2022-01-09',
      '2022-04-10',
      '16:00',
      1,
      22,
      1,
      2,
      256
   ),
   (
      'Advanced Steps',
      '2021-01-09',
      '2021-06-10',
      '18:00',
      2,
      22,
      2,
      2,
      374
   ),
   (
      'Advanced Steps',
      '2021-09-09',
      '2021-12-09',
      '17:00',
      2,
      12,
      1,
      2,
      204
   ) ON CONFLICT (name, startdate, enddate, time, room_id) DO NOTHING;
INSERT INTO courseenrolments (course_id, user_id)
VALUES 
(3, 'immi@hei.com'),
(4, 'erik@heida.com'),
(3, 'erik@heida.com'),
(1, 'enna@heida.com'),
(1, 'ennalisa@heida.com'),
(1, 'mimmi@cool.com'),
(1, 'eve@hot.com'),
(1, 'maria@hot.com'),
(1, 'carla@calle.com'),
(1, 'carlise@calle.com'),
(1, 'gwyn@hi.com') ON CONFLICT (course_id, user_id) DO NOTHING;


