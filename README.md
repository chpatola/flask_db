# Flask App with a Postgres Database: Dance School Enrolment System

## About
This application is made within  the course "Tietokantasovellus" at University of Helsinki. It enables persons interested in learning modern jazz dance to sign up for dance classes offered by Aida Dance School. 
The app also has a admin section where the courses and enrolments can be managed.
You can use it here: https://aidadanceschool.herokuapp.com

#### Admin
info@aidadanceschool.com & aidarocks_

#### Student
student12@student.com & <3aidadance

## Deployment Instructions (for learning purposes)

### Develop and test locally
1. Clone this git repository to your computer
2. Download pg-install.sh from https://github.com/hy-tsoha/local-pg and run it according to the instructions
3. cd into the folder for this repo
4. create an .env file with DATABASE_URL and SECRET_KEY
5. Run the setup file (I need to fix that!) and open the local version of the app in http://127.0.0.1:5000/ 

### Publish to Heroku
1. Create a free account at Heroku
2. Create a new app with a name of your choice
3. Provision postgres database in heroku
.... (More to come)

## Functionality and Database Structure

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
 * COURSES((pk) id:serial, startdate:date, finishdate:date,time:time, durationhour:float, occurances:int, (fk) teacherid -> Teachers, (fk) roomid -> Rooms)
 * COURSESENROLMENT((pk) id:serial, (fk) courseid -> Courses,(fk) userid -> Users - On delete set null)
 
## Progression Diary
 
### Progression 26.9
The base functionality of the application is almost finished. What is missing is the admin's ability to delete a course. After that is set up, I will improve the stability of the app (validating input, error catching).

