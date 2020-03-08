CREATE TABLE book (
  id serial,
  title varchar(100) NOT NULL,
  author varchar(40) NOT NULL,
  year integer NOT NULL,
  isbn varchar(10) UNIQUE,
  review_count integer,
  average_score numeric
);

CREATE TABLE userr (
  id serial,
  username varchar(40) NOT NULL,
  password varchar(20) NOT NULL,
  fullname varchar(40),
  email text,
  day_register date
);

CREATE TYPE  rate AS ENUM ('1', '2', '3', '4', '5');
CREATE TABLE rating (
  id serial,
  book_id integer NOT NULL,
  userr_id integer NOT NULL,
  star rate,
  rating_day date,
  opinion text
);
