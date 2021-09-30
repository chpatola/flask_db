# Flask App with a Postgres Database: Dance School Enrolment System

## About
This application is made within  the course "Tietokantasovellus" at University of Helsinki. It enables persons interested in learning modern jazz dance to sign up for dance classes offered by Aida Dance School. 
The app also has a admin section where the courses and enrolments can be managed.
You can use it here: https://aidadanceschool.herokuapp.com

#### Admin
info@aidadanceschool.com & aidarocks_

#### Student
student12@student.com & <3aidadance

## Deployment Instructions (to be used for learning, not in production)

### Develop and test locally
1. Clone this git repository to your computer
2. Download pg-install.sh from https://github.com/hy-tsoha/local-pg and run it according to the instructions
3. cd into the folder for this repo
4. create an .env file with 
* DATABASE_URL=postgresql:///user"
* SECRET_KEY= the result you get when you run the following in python
```
import secrets
>>> secrets.token_hex(16)
```
5. Create a virtual environment for this project ( I use conda) and install the required packages (I use pip):
``` 
conda create --name <yourname>
conda activate <yourname>
pip install -r requirements.txt

```
6. Start the database:
```
start-pg.sh
```
7. Open a new terminal and populate the database with the default tables and base data:
```
psql < db_setup.sql
```

8. Run the app as shown below and then open the local version of the app in http://127.0.0.1:5000/ 
```
export FLASK_ENV=development #This will a.o. restart the server when you make changes in the code
flask run

```
9. Develop the code and see the changes in your browser. If you haven't already, init a new git repo (git init) and make regular commits

### Publish to Heroku
1. If you do not already have one, create a free account at heroku.com
2. Create a new app with a name of your choice
3. Login to Heroku in the terminal and attach your git repo to heroku
```
heroku login

heroku git:remote -a <nameofyourapp>
```
4. Create a Postgres database in Heroku and populate it wit our tables and test data. Add the secret key to it
``` 
heroku addons:create heroku-postgresql
heroku psql < db_setup.sql
heroku config:set SECRET_KEY=<yoursecretkeyhere>
``` 
5. Publish the app in Heroku. Heroku will inform you about the url wher you can use it
```
git push heroku main
```

## Functionality and Database Structure

### Main functionality for Students
 * See an overview of upcoming courses 
 * Register for a course
 * Remove the registration. This is possible if the course has not yet started
 * Create a personal profile 
 * Edit the personal profile
 * Delete the personal profile. This is possible if the user is not registered to an ongoing or upcoming course

### Main functionality for Admins
 * See an overview of ongoing and upcoming courses 
 * Create a new course
 * Delete a course. This is possible if there is no registrations for the course
 * List students
 * List teachers
 * Add teachers
 * List dance rooms
 
 ### Database Structure (see specifics in db_setup.sql)
 
 * USERS((pk) username:string, password:string, firstname:string, lastname:string, phone:string, bornyear:integer, usertype:string, removed: boolean) 
 * TEACHERS((pk) id:serial,firstname:string, lastname:string, email:string, hourlysalary:float)
 * ROOMS((pk) id:serial, m2:float, capacity:int)
 * COURSES((pk) id:serial, startdate:date, finishdate:date,time:time, durationhour:float, occurances:int, (fk) teacherid -> Teachers, (fk) roomid -> Rooms)
 * COURSESENROLMENT((pk) id:serial, (fk) courseid -> Courses,(fk) userid -> Users - On delete set null)
 
## Progression Diary
 
### Progression 26.9
The base functionality of the application is almost finished. What is missing is the admin's ability to delete a course. After that is set up, I will improve the stability of the app (validating input, error catching).

### Progression 10.10
