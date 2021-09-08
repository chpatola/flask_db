# Flask App with a Database: Dance School Enrolment System
An application made within the course "Tietokantasovellus" at University of Helsinki

## About

This application enables persons interested in learning modern dance jazz to sign up for dance classes offered by Aida Dance School. The app also has a admin section where the courses and enrolments can be managed.

### Main functionality for Students
 * See an overview of upcoming courses 
 * Register for a course
 * Remove the registration. This is possible if the course has not yet started
 * Create a personal profile 
 * Edit the personal profile
 * Delete the personal profile. This is possible if the user is not registered to an ongoing or upcoming course

### Main functionality for Admins
 * See an overview of ongoing and upcoming  courses 
 * Create a new course
 * Delete a course. This is possible if there is no registrations for the course
 * List students
 * List teachers
 * Add teachers
 
 ### Database Structure
 
 * USERS((pk) username:string, password:string, firstname:string, lastname:string, phone:string, bornyear:integer, usertype:string, removed: boolean) 
 * TEACHERS((pk) id:serial,firstname:string, lastname:string, email:string, hourlysalary:float)
 * ROOMS((pk) id:serial, m2:float, capacity:int)
 * COURSES((pk) id:serial, startdate:date, finishdate:date,time:time, durationhour:float, occurances:int, (fk) roomid -> Rooms)
 * COURSESENROLMENT((pk) id:serial, (fk) courseid -> Courses,(fk) userid -> Users - On delete set null)
 
