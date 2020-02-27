-- Primary KEY
ALTER TABLE book ADD
CONSTRAINT pk_book PRIMARY KEY (id);

ALTER TABLE userr ADD
CONSTRAINT pk_user PRIMARY KEY (id);

ALTER TABLE rating ADD
CONSTRAINT pk_rating PRIMARY KEY (id);

-- Set reference key for relationship
ALTER TABLE rating ADD
CONSTRAINT fk_rating_book FOREIGN KEY book_id REFERENCES book;

ALTER TABLE rating ADD
CONSTRAINT fk_rating_user FOREIGN KEY user_id REFERENCES user;
