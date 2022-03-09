import psycopg2
import os


def dbConnection():
  db = os.environ['POSTGRES_NAME']
  user = os.environ['POSTGRES_USER']
  password = os.environ['POSTGRES_PASSWORD']
  host = 'localhost'
  connection = psycopg2.connect(host=host, database=db, user=user, password=password)
  return connection

def emailExists(cursor, email):
  lowercase = email.lower()
  query = "SELECT EXISTS (SELECT 1 FROM users WHERE cannonical_email=%(user_input)s);"
  cursor.execute(query, {"user_input": lowercase})
  return cursor.fetchone()[0] == 1

def insertUser(cursor, email, password_digest):
  cannonical_email = email.lower()
  query = """
  INSERT INTO users (email, password_digest, cannonical_email)
  VALUES (%(email)s, %(password_digest)s, %(cannonical_email)s);
  """
  cursor.execute(query, {'email': email, 'password_digest': password_digest, 'cannonical_email': cannonical_email})

createUserIDSequence = """
CREATE SEQUENCE IF NOT EXISTS UserIDSequence;
"""

createUsersTable = """
CREATE TABLE users
(
  id SERIAL PRIMARY KEY
  email TEXT,
  cannonical_email TEXT UNIQUE,
  password_digest INT
);
"""



if __name__ == "__main__":
  conn = dbConnection()
  with conn.cursor() as curs:
    curs.execute(createUserIDSequence)
    curs.execute(createUsersTable)
    insertUser(curs, 'testmail@gmail.com', 1234)
