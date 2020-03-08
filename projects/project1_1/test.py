from flask import Flask, session, render_template, jsonify, request
from model import *
from sqlalchemy import and_

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = '25050000000000000000111zzz'
app.config['SESSION_TYPE'] = 'filesystem'
db.init_app(app)


@app.route("/test", methods=["GET"])
def get_info():
    username = "hello"
    password = "hello"
    userr = Userr.query.filter(username="hello").all()
    print(userr)
    return "Hello World !"
