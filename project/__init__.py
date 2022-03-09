from enum import unique
from flask import Flask, request, jsonify, g

import flask_sqlalchemy
import os
import psycopg2





def create_app(test_config=None):
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
  db = flask_sqlalchemy.SQLAlchemy(app)

  class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    def __repr__(self):
      return f"{self.id} {self.email} {self.password}"
    

  db.create_all()

  @app.route("/signup", methods=["POST"])
  def signUp():
    email = request.json['email']
    password = request.json['password'] #TODO hash this
    db.session.add(User(email=email, password=password))
    db.session.commit()
    return '200'
    


  @app.route("/users")
  def getAll():
    all_users = db.session.query(User).all()
    ret = [{'id': user.id, 'email': user.email, 'password': user.password} for user in all_users]
    return jsonify(ret)


  @app.route('/')
  def index():
    return 'wizards rule'

  return app