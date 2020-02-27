import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    with open("books.csv") as f:
        print("Opened successfully")
        reader = csv.reader(f)

        # Skip the first line
        next(f)

        for line in reader:
            print(line)
            db.execute("INSERT INTO book (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                        {"isbn": line[0], "title": line[1], "author": line[2], "year": line[3]})

            print(f"Added book of author {line[2]} having title is {line[1]}, published in {line[3]} with isbn code: {line[0]}")
            line_number += 1

        db.commit()
        print(f"Added data successfully !\
                \nThere are {line_number} record insered")
        return

    print("Can't open file !")

if __name__ == "__main__":
    main()
