add_teacher = "INSERT INTO teacherstest (LASTNAME, FIRSTNAME, PHONE, EMAIL, HOURLYSALARY) VALUES (:firstname, :lastname, :phone, :email, :hourlysalary)"

add_user = "INSERT INTO userstest VALUES (:username, :password, :firstname, :lastname, :phone, :bornyear, :usertype, :removed)"

check_users_course = "SELECT COUNT(ID) AS AMOUNT FROM COURSEENROLMENTSTEST WHERE USER_ID = :username"

courses_all ="WITH ENROLMENTS AS (SELECT COURSE_ID,COUNT(USER_ID) AS ENROLLED_STUDENTS" \
   " FROM COURSEENROLMENTSTEST GROUP BY COURSE_ID)"\
" SELECT C.ID,C.NAME,C.STARTDATE,C.ENDDATE,C.TIME, C.DURATIONHOUR, C.OCCURANCES," \
   "CONCAT(T.LASTNAME, ', ', T.FIRSTNAME) AS TEACHER_NAME,R.NAME AS ROOM_NAME,E.ENROLLED_STUDENTS,"\
   "CASE WHEN R.CAPACITY - E.ENROLLED_STUDENTS < 1 THEN 'Full'ELSE 'Spot(s) available' END AS STATUS" \
" FROM COURSESTEST C LEFT JOIN TEACHERSTEST T ON T.ID = C.TEACHER_ID" \
" LEFT JOIN ROOMSTEST R ON R.ID = C.ROOM_ID LEFT JOIN ENROLMENTS E ON E.COURSE_ID = C.ID"\
   " WHERE STARTDATE >= CURRENT_DATE ORDER BY STARTDATE"

courses_user ="SELECT C.ID,C.NAME,C.STARTDATE,C.ENDDATE,C.TIME, C.DURATIONHOUR, C.OCCURANCES," \
   "CONCAT(T.LASTNAME, ', ', T.FIRSTNAME) AS TEACHER_NAME,R.NAME AS ROOM_NAME"\
" FROM COURSESTEST C LEFT JOIN TEACHERSTEST T ON T.ID = C.TEACHER_ID" \
" LEFT JOIN ROOMSTEST R ON R.ID = C.ROOM_ID WHERE C.ID IN (SELECT DISTINCT COURSE_ID" \
   " FROM COURSEENROLMENTSTEST WHERE USER_ID=:user_id AND (STARTDATE > CURRENT_DATE OR ENDDATE <= CURRENT_DATE)) ORDER BY STARTDATE"

find_user = "SELECT username, password, firstname, usertype FROM userstest WHERE username=:username AND removed = FALSE"

remove_user = "UPDATE USERSTEST SET REMOVED = TRUE WHERE USERNAME=:username "

rooms = "SELECT ID, NAME, M2,CAPACITY FROM ROOMSTEST"

teachers = "SELECT ID, LASTNAME, FIRSTNAME, PHONE, EMAIL, HOURLYSALARY FROM TEACHERSTEST"