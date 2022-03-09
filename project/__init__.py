from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
import os
import psycopg2




def emailExists(cursor, email):
  lowercase = email.lower()
  query = "SELECT EXISTS (SELECT 1 FROM users WHERE email=%(user_input)s);"
  cursor.execute(query, {"user_input": lowercase})
  return cursor.fetchone()[0] == 1

def insertUser(curs, email, password_digest):
  query = """
  INSERT INTO users (email, password_digest)
  VALUES (%(email)s, %(password_digest)s);
  """
  curs.execute(query, {'email': email, 'password_digest': password_digest})


def digestPassword(password):
  return int(password)


def create_app(test_config=None):
  app = Flask(__name__)

  def getDB():
    db = getattr(g, '_database', None)
    if db is None:
      user = os.environ['POSTGRES_USER']
      database = os.environ['POSTGRES_DB']
      password = os.environ['POSTGRES_PASSWORD']
      host = 'db'
      db = g._database = psycopg2.connect(host=host, dbname=database, user=user, password=password)
    return db

  @app.teardown_appcontext
  def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
      db.commit() #this is here to make transactions commit, the docs suggest this should happen when a cursor is used as a context manager though so I'm unsure of what is wrong
      db.close()

  @app.route("/signup", methods=["PUT"])
  def signUp():
    email = request.json['email']
    password = request.json['password']
    conn = getDB()
    with conn.cursor() as curs:
      if emailExists(curs, email) == False:
        digest = digestPassword(password) #TODO that auth and password stuff
        print(email, digest)
        insertUser(curs, email, digest) #should function return value or otherwise handle errors here?
        return '200'
      else:
        return '400'
    


  @app.route("/users")
  def getAll():
    conn = getDB()
    with conn.cursor() as curs:
      query = "SELECT * FROM users;"
      ret = ''
      curs.execute(query)
      for row in curs.fetchall():
        ret += str(row) + '<br>'
      return ret

  @app.route('/')
  def index():
    return 'wizards rule'

  return app