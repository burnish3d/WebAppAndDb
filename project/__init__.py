from enum import unique
from flask import Flask, request, jsonify, g, session, redirect, abort, url_for
from flask_login import UserMixin, LoginManager, login_user, current_user, login_required, logout_user
import bcrypt
import flask_sqlalchemy
import os
import psycopg2



lm = LoginManager()

def create_app(test_config=None):
  app = Flask(__name__)
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
  app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or '8aa7260d1028ae38f6e978dee5a1e0e80c02bc94de74096e'
  db = flask_sqlalchemy.SQLAlchemy(app)
  lm.init_app(app)

  
  class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
      return f"{self.id} {self.email} {self.password_hash}"
    

  db.create_all()

  @lm.user_loader
  def load_user(id):
    return User.query.get(id)

  @lm.unauthorized_handler
  def unauthorized():
    return abort('401', description="Not authorized")


  @app.route("/signup", methods=["POST"])
  def signUp():
    email = request.json['email']
    if User.query.filter_by(email=email).first(): return '400'
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
      login_user(real_user)
      return redirect(url_for('secrets'), code=418)

    return abort(401, description='Login failed')

  @app.route('/logout')
  @login_required
  def logout():
    logout_user()
    return redirect('/')

  @app.route("/users")
  def getAll():
    all_users = db.session.query(User).all()
    ret = [{'id': user.id, 'email': user.email, 'password_hash': user.password_hash.decode('utf-8')} for user in all_users]
    return jsonify(ret)

  @app.route("/secrets")
  @login_required
  def secrets():
    return f"Welcome to the inner sanctum, {current_user.email.split('@')[0]}"


  @app.route('/')
  def index():
    if current_user.is_authenticated:
      return f"Welcome, {current_user.email.split('@')[0]}"
    else:
      return f"Well howdy stranger"

  return app