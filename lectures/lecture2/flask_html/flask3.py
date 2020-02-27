from flask import Flask, render_template, request

app = Flask(__name__)

names = list()

@app.route("/")
def index():
    return render_template("index3.html")

@app.route("/hello", methods=["POST"])
def hello():
    name = request.form.get("name")
    return render_template("hello.html", name=name)
