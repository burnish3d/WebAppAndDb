from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2
from db_init import insertUser, emailExists, dbConnection




def digestPassword(password):
  return int(password)

app = Flask(__name__)

@app.route("/signup", methods=["PUT"])
def signUp():
  email = request.json['email']
  password = request.json['password']
  conn = dbConnection()
  cursor = conn.cursor()
  with conn.cursor() as curs:
    if emailExists(cursor, email) == False:
      digest = digestPassword(password) #TODO that auth and password stuff
      insertUser(curs, email, digest) #should function return value or otherwise handle errors here?
      return "200"
    else:
      return "404"

@app.route("/users")
def getAll():
  cursor = dbConnection.cursor()
  query = "SELECT * FROM users;"
  ret = ''
  for row in cursor.execute(query).fetchall():
    ret += str(row)
  return ret

@app.route('/')
def index():
  return 'welcome'