from enum import unique
from flask import Flask, request, jsonify, g
import bcrypt
import flask_sqlalchemy
import os
import psycopg2
from flask_login import LoginManager




def create_app(test_config=None):
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
  db = flask_sqlalchemy.SQLAlchemy(app)

  class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
      return f"{self.id} {self.email} {self.password_hash}"
    

  db.create_all()

  @app.route("/signup", methods=["POST"])
  def signUp():
    email = request.json['email']
    password = request.json['password']
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt) #this step silently ignores passwords longer than 72 characters, and we are goingto treat all input as utf-8 for now
    db.session.add(User(email=email, password_hash=hash))
    db.session.commit()
    return '200'
    
  @app.route("/login")
  def login():
    email = request.json['email']
    password = request.json['password']
    real_user = User.query.filter_by(email=email).first()
    if real_user and bcrypt.checkpw(password.encode('utf-8'), real_user.password_hash):
      #do something? auth token of some kind?
      return '200'
    return '401'


  @app.route("/users")
  def getAll():
    all_users = db.session.query(User).all()
    ret = [{'id': user.id, 'email': user.email, 'password_hash': user.password_hash.decode('utf-8')} for user in all_users]
    return jsonify(ret)


  @app.route('/')
  def index():
    return 'wizards rule'

  return app