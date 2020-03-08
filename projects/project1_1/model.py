import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String, nullable=False, unique=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=True)
    review_count = db.Column(db.Integer, default=0)
    average_score = db.Column(db.Float, default=0)


class Userr(db.Model):
    __tablename__ = "userr"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    fullname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, key='email')
    day_register = db.Column(db.DateTime, default="NOW()")


class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=True)
    userr_id = db.Column(db.Integer, db.ForeignKey("userr.id"), nullable=False)
    rating_day = db.Column(db.DateTime, server_default="NOW()")
    star = db.Column(db.String, default=0)
    opinion = db.Column(db.String, nullable=False)


    def add_rating(book_id:int, userr_id:int, star:int, opinion:str):
        rating = Rating(book_id=book_id, userr_id=userr_id, star=star,opinion=opinion)
        db.session.add(rating)
        db.session.commit()

def main():
    db.createAll()

if __name__ == "__main__":
    main()
