import os
from datetime import date

from flask import Flask, session, request, render_template, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify # <- `jsonify` instead of `json`


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        books = db.execute("SELECT isbn, title, author, year, review_count, average_score FROM book LIMIT 10").fetchall()
        for book in books:
            print(book)
        return render_template("home.html", books=books)


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("registration.html")
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        repassword = request.form.get("repassword")
        fullname = request.form.get("fullname")
        email = request.form.get("email")

        if password != repassword:
            password_error = "The re-enter password not matched with the password !"
            return render_template("registration.html", password_error=password_error)

        print("Info: ", username, password, fullname, email)
        try:
            db.execute("INSERT INTO userr (username, password, fullname, email) VALUES (:username, :password, :fullname, :email)",
                            {"username": username, "password": password, "fullname": fullname, "email":email})
            db.commit()
        except:
            message = "Invalid information ! Try again !"
            return render_template("registration.html", message=message)
        return render_template("sucessful.html", username=username)


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        session["user"] = db.execute("SELECT * FROM userr WHERE username = :username AND password = :password",
                                {"username": session["username"], "password": session["password"]}).fetchall()
        if not session["user"]:
            session.clear()
            message = "Invalid login or password. Please try again !"
            return render_template("login.html", message=message)
        # If the login is success, return the page of user
        print(session["user"])
        return render_template("login_sucessful.html")

    if request.method == "GET":
        message = "Enter your username account and password !"
        return render_template("login.html", message=message)

@app.route("/drashboard", methods=["GET"])
def drashboard():
    ratings = db.execute("SELECT * FROM userr, rating, book WHERE userr.id=rating.userr_id AND rating.book_id=book.id AND userr.username=:username",
                            {"username": session["username"]}).fetchall()
    if request.method == "GET":
        return render_template("drashboard.html", ratings=ratings)

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        try:
            session["book"] = db.execute("SELECT * FROM book WHERE book.isbn=:isbn",
                                        {"isbn": isbn}).fetchone()
        except:
            message_error = "Invalid isbn code. Try again !"
            return render_template("home.htlm", message_search=message_search)
        else:
            session["rating_info"] = db.execute("SELECT userr.username, rating.star, rating.opinion, rating.rating_day FROM book, userr, rating WHERE book.id=rating.book_id AND userr.id=userr_id AND book.isbn=:isbn",
                                        {"isbn": isbn}).fetchall()
            return render_template("book.html", book=session["book"])

    if request.method == "GET":
        return redirect(url_for('search'))

@app.route("/commend/", methods=["POST"])
def commend():
    if request.method == "POST":
        try:
            print(session["user"][0][0])
        except:
            return render_template("commendfail.html")
        else:
            star = request.form.get("star")
            opinion = request.form.get("opinion")
            print(session["book"])
            db.execute("INSERT INTO rating (book_id, userr_id, star, opinion) VALUES (:book_id, :userr_id, :star, :opinion)",
                            {"book_id": session["book"][0], "userr_id": session["user"][0][0], "star": star, "opinion": opinion})
            db.commit()
            session["rating_info"] = db.execute("SELECT userr.username, rating.star, rating.opinion, rating.rating_day FROM book, userr, rating WHERE book.id=rating.book_id AND userr.id=userr_id AND book.isbn=:isbn",
                                    {"isbn": session["book"][0]}).fetchall()

            commend_success = "You have reviewed the book ! Thank you for your opinion !"
            return render_template("book.html", commend_success=commend_success)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        session["user"] = db.execute("SELECT * FROM userr WHERE username=:username", {"username": session["username"]}).fetchone()
        print(session["user"])
        return render_template("user.html")

# API for detail book
@app.route("/api/books/<int:isbn>")
def flight_api(isbn):
    """Return details about a single flight."""

    # Make sure flight exists.
    book = db.execute("SELECT book.title, book.author, book.year, book.review_count, book.average_score FROM book WHERE book.isbn=:isbn",
                        {"isbn": str(isbn)}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 422

    return jsonify(dict(book))
