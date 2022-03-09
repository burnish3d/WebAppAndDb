
CREATE TABLE IF NOT EXISTS users
(
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL,
  password_digest INT
);

INSERT into users (email, password_digest) VALUES('testmail@gmail.com', 1234);
Insert into users (email, password_digest) VALUES('bad4u@gmail.com', 5);
Insert into users (email, password_digest) VALUES('goodforme@gmail.com', 18);
