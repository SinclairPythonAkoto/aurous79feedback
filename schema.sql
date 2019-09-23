DROP TABLE if exists aurous_feedback;
CREATE TABLE aurous_feedback (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  age INTEGER,
  sex VARCHAR,
  first_visit VARCHAR,
  return_visit VARCHAR,
  cleanliness INTEGER,
  customer_service INTEGER,
  speed INTEGER,
  shisha VARCHAR,
  comment VARCHAR,
  email VARCHAR,
  date_stamp VARCHAR NOT NULL
  );

DROP TABLE if exists email_library;
CREATE TABLE email_library (
  id SERIAL PRIMARY KEY,
  name VARCHAR,
  email VARCHAR
  )
