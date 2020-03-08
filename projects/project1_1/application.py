from flask import Flask, session, render_template, jsonify, request, redirect, url_for
from model import *
from sqlalchemy import and_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Fix error:
# RuntimeError: The session is unavailable because no secret key was set.
# Set the secret_key on the application to something unique and secret.
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db.init_app(app)


@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        try:
            top_books = list(Book.query.limit(10).all())
        except:
            return render_template('404.html')
        else:
            return render_template('home.html', top_books=top_books)


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
        try:
            userr = Userr(username=username, password=password, fullname=fullname, email=email)
            db.session.add(userr)
            db.session.commit()
        except:
            message = "Invalid information ! Try again !"
            return render_template("registration.html", message=message)
        return render_template("sucessful.html", username=username)


@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        print(username, password)
        try:
            # Error : typeerror: object of type is not json serializable
            # session["userr"] = Userr.query.filter(and_(Userr.username==username, Userr.password==password)).all()
            session["userr"] = dict(db.session.execute("SELECT id, username, password, fullname, email, day_register FROM userr WHERE userr.username=:username and userr.password=:password",
                                                {"username": username, "password": password}).fetchone())
            # dict() để ép kiểu tuple về dictionary cho việc truy cập giá trị dễ dàng.
        except:
            message = "Invalid login or password. Please try again !"
            return render_template("login.html", message=message)
        else:
            return render_template("login_successful.html")

    if request.method == "GET":
        message = "Enter your username account and password !"
        return render_template("login.html", message=message)


@app.route("/drashboard", methods=["GET"])
def drashboard():
    user_ratings =  db.session.query(Book, Userr, Rating).filter(and_(Book.id == Rating.book_id, Userr.id == Rating.userr_id, Userr.id == session["userr"]["id"])).all()
    if request.method == "GET":
        return render_template("drashboard.html", user_ratings=user_ratings)

@app.route("/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        isbn = request.form.get("isbn")
        try:
            book = Book.query.filter_by(isbn=isbn).first()
        except:
            return render_template('404.html')
        else:
            if book is None:
                message_search = "Invalid isbn code. Try again !"
                return render_template("home.html", message_search=message_search)
            else:
                rating_info = db.session.query(Book, Userr, Rating).filter(and_(Book.id==Rating.book_id, Userr.id==Rating.id, Book.isbn==isbn)).all()
                return render_template("book.html", book=book, rating_info=rating_info)


@app.route("/commend/<int:book_id>", methods=["POST"])
def commend(book_id):
    if request.method == "POST":
        try:
            print(session["userr"])
        except:
            return render_template("commendfail.html")
        else:
            star = str(request.form.get("star"))
            opinion = str(request.form.get("opinion"))
            print(opinion)
            book = Book.query.filter_by(id=book_id).first()
            if star and opinion:
                Rating.add_rating(book_id=book_id, userr_id=session['userr']['id'], star=star, opinion=opinion)
                rating_info = db.session.query(Rating, Userr, Book).filter(and_(Rating.book_id==book_id, Userr.id==Rating.userr_id, Book.id==book_id)).all()
                commend_success = "You have commended for the book ! Thank you for your rating !"
                return render_template("book.html", book=book, commend_success=commend_success, rating_info=rating_info)
            else:
                return render_template('book.html', book=book)

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/user", methods=["GET", "POST"])
def user():
    if request.method == "GET":
        print(session["userr"])
        return render_template("user.html")

# API for detail book
@app.route("/api/books/<int:isbn>")
def flight_api(isbn):
    """Return details about a single flight."""

    # Make sure flight exists.
    book = Book.query.filter_by(isbn=str(isbn))
    if book is None:
        return jsonify({"error": "Invalid isbn"}), 422
    return jsonify(dict(book))
