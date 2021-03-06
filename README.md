<h3 align="center">WebAppAndDb</h3>

## About The Project

This project supports cookie based authentication in a Flask web app and offers five end points to test functionality
/signup to register with the service, /users to verify storage of user credentials, /login to recieve the cookie credential
/secrets to demonstrate different behavior for authenticated and unauthenticated users, and /logout to expire your session.

This was done as part of a take home interview and includes a docker-compose.yml that will start a PostgreSQL database and Flask webapp. I spent more time wrangling Docker than was strictly necessary but I enjoyed the process and all the things I learned on the way.

### What do I do with this?

Nothing yet! I think this project will work itself towards being a reasonably generic example of a web app and database, something you or I would just fork as the basis of another project.

### Built With

* [Python3](https://www.python.org/downloads/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [Docker & Docker Compose](https://www.docker.com/)
* [SQAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Postgresql](https://www.postgresql.org/)

### INSERT SQL SCHEMA 
The schema was generated by SQLAlchemy and captured from the terminal output as follows

CREATE TABLE users (
       id SERIAL NOT NULL, 
       email VARCHAR NOT NULL, 
       cannonical_email VARCHAR NOT NULL, 
       password_hash BYTEA NOT NULL, 
       PRIMARY KEY (id), 
       UNIQUE (email), 
       UNIQUE (cannonical_email)
)

### How do I run this?

To run, and guarantee that you see the results of any local changes after editing, invoke

```
docker-compose up --build
```
Run it in detached mode -d if you do not want the output to be redirected to that terminal. 

### How do I stop this?

```
docker-compose down
```
Will stop and remove the containers but not any associated volumes.


### API documentation

[Postman Collection](https://www.getpostman.com/collections/65662e06361f104400f2)
