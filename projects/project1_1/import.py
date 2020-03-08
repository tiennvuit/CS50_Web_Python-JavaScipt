import os
import csv
from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open("database/books.csv") as f:
        print("Opened successfully !")
        # Skip the first line
        next(f)
        count = 0
        reader = csv.reader(f)
        for  isbn, title, author, year in reader:
            print(isbn, title, author, year)
            book = Book(isbn=isbn, title=title, author=author, year=year)
            db.add(book)
            count += 1
            if count == 10:
                db.commit()
                count = 0
                print(f"Added 10 books successfully !")
        print("Oke !")

if __name__ == "__main__":
    main()
