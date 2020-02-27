from flask import Flask, render_template, request

app = Flask(__name__)

names = list()

@app.route("/")
def index():
    return render_template("index4.html")


@app.route("/hello1", methods=["POST", "GET"])
def hello1():
    if request.method == "GET":
        return render_template("index4.html")
    name = request.form.get("name")
    names.append(name)
    return render_template("hello1.html", names=names)
