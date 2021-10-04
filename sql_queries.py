"""SQL queries used by routes.py"""
add_course = "INSERT INTO courses (NAME, STARTDATE, ENDDATE, TIME, OCCURANCES, DURATIONHOUR, PRICE, TEACHER_ID, ROOM_ID)"\
   " VALUES (:name, :startdate, :enddate, :time, :occurances, :duration, :price, :teacher_id, :room_id)" 

add_teacher = "INSERT INTO teachers (LASTNAME, FIRSTNAME, PHONE, EMAIL, HOURLYSALARY) VALUES (:firstname, :lastname, :phone, :email, :hourlysalary)"

add_user = "INSERT INTO users VALUES (:username, :password, :firstname, :lastname, :phone, :bornyear, :usertype, :removed)"

check_users_course = "SELECT COUNT(ID) AS AMOUNT FROM COURSEENROLMENTS WHERE USER_ID = :username  AND COURSE_ID = :id"

check_users_courses = "SELECT COUNT(ID) AS AMOUNT FROM COURSEENROLMENTS WHERE USER_ID = :username"

courses_ongoing = "WITH ENROLMENTS AS (SELECT COURSE_ID,COUNT(USER_ID) AS ENROLLED_STUDENTS" \
   " FROM COURSEENROLMENTS GROUP BY COURSE_ID)"\
" SELECT C.ID,C.NAME,C.STARTDATE,C.ENDDATE,C.TIME, C.DURATIONHOUR, C.OCCURANCES," \
   "CONCAT(T.LASTNAME, ', ', T.FIRSTNAME) AS TEACHER_NAME,R.NAME AS ROOM_NAME,"\
" COALESCE(E.ENROLLED_STUDENTS, 0) AS ENROLLED_STUDENTS,"\
   "CASE WHEN R.CAPACITY - E.ENROLLED_STUDENTS < 1 THEN 'Full'ELSE 'Spot(s) available' END AS STATUS, C.PRICE" \
" FROM COURSES C LEFT JOIN TEACHERS T ON T.ID = C.TEACHER_ID" \
" LEFT JOIN ROOMS R ON R.ID = C.ROOM_ID LEFT JOIN ENROLMENTS E ON E.COURSE_ID = C.ID"\
   " WHERE STARTDATE <= CURRENT_DATE AND ENDDATE >= CURRENT_DATE ORDER BY STARTDATE, NAME"

courses_upcoming = "WITH ENROLMENTS AS (SELECT COURSE_ID,COUNT(USER_ID) AS ENROLLED_STUDENTS" \
   " FROM COURSEENROLMENTS GROUP BY COURSE_ID)"\
" SELECT C.ID,C.NAME,C.STARTDATE,C.ENDDATE,C.TIME, C.DURATIONHOUR, C.OCCURANCES," \
   "CONCAT(T.LASTNAME, ', ', T.FIRSTNAME) AS TEACHER_NAME,R.NAME AS ROOM_NAME,"\
   " COALESCE(E.ENROLLED_STUDENTS,'0') AS ENROLLED_STUDENTS,"\
   " CASE WHEN R.CAPACITY - E.ENROLLED_STUDENTS < 1 THEN 'Full'ELSE 'Spot(s) available' END AS STATUS, C.PRICE" \
" FROM COURSES C LEFT JOIN TEACHERS T ON T.ID = C.TEACHER_ID" \
" LEFT JOIN ROOMS R ON R.ID = C.ROOM_ID LEFT JOIN ENROLMENTS E ON E.COURSE_ID = C.ID"\
   " WHERE STARTDATE >= CURRENT_DATE ORDER BY STARTDATE, NAME"

courses_user = "SELECT C.ID,C.NAME,C.STARTDATE,C.ENDDATE,C.TIME, C.DURATIONHOUR, C.OCCURANCES," \
   "CONCAT(T.LASTNAME, ', ', T.FIRSTNAME) AS TEACHER_NAME,R.NAME AS ROOM_NAME, C.PRICE"\
" FROM COURSES C LEFT JOIN TEACHERS T ON T.ID = C.TEACHER_ID" \
" LEFT JOIN ROOMS R ON R.ID = C.ROOM_ID WHERE C.ID IN (SELECT DISTINCT COURSE_ID" \
   " FROM COURSEENROLMENTS WHERE USER_ID=:user_id AND (STARTDATE > CURRENT_DATE OR ENDDATE <= CURRENT_DATE)) ORDER BY STARTDATE"

disenrol_course = "DELETE FROM COURSEENROLMENTS WHERE USER_ID=:username AND COURSE_ID =:id"

edit_user = "UPDATE USERS SET FIRSTNAME=:firstname, LASTNAME=:lastname,PHONE=:phone,BORNYEAR=:bornyear"\
   " WHERE USERNAME=:username"

edit_userpsw = "UPDATE USERS SET PASSWORD=:newpassword, FIRSTNAME=:firstname, LASTNAME=:lastname,PHONE=:phone,BORNYEAR=:bornyear"\
   " WHERE USERNAME=:username"

enrol_course = "INSERT INTO COURSEENROLMENTS (COURSE_ID, USER_ID) VALUES (:id, :username)"

find_user = "SELECT username, password, firstname, usertype FROM users WHERE username=:username AND removed = FALSE"

remove_course = "DELETE FROM  COURSES WHERE ID =:id"

remove_user = "UPDATE USERS SET REMOVED = TRUE WHERE USERNAME=:username"

rooms = "SELECT ID, NAME, M2,CAPACITY FROM ROOMS"

teachers = "SELECT ID, LASTNAME, FIRSTNAME, CONCAT(LASTNAME, ', ', FIRSTNAME) AS NAME, PHONE, EMAIL, HOURLYSALARY FROM TEACHERS"


userdata = "SELECT USERNAME, FIRSTNAME, LASTNAME, PHONE, BORNYEAR FROM USERS WHERE USERNAME=:username"

users_course = "SELECT U.USERNAME,U.FIRSTNAME,U.LASTNAME,U.PHONE,U.BORNYEAR FROM COURSEENROLMENTS E" \
    " LEFT JOIN USERS U ON U.USERNAME = E.USER_ID WHERE E.COURSE_ID = :id"
    