
from flask import Flask, render_template, request, session # gives access to a variable called `session`
                                                           # which can be used to keep vaules that are specific to a particular user
from flask_session import Session # an additional extension to sessions which allows them
                                  # to be stored server-side
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("notes") is None:
        session["notes"] = []
    if request.method == "POST":
        note = request.form.get("note")
        session["notes"].append(note)

    return render_template("hello2.html", notes=session["notes"])
