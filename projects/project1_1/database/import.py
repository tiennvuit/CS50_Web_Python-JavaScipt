import os
import csv
from model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open("books.csv") as f:
        print("Opened  successfully !")
        reader = csv.reader(f)
        # Skip the first line
        next(f)
        for  isbn, title, author, year in reader:
            book = Book(isbn=isbn, title=title, author=author, year=year)
            db.session.add(book/)
            print(f"Added book successfully")

if __name__ == "__main__":
    main()
