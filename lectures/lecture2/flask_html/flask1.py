from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def hello():
	return "<h1>Hello World </h1>"


@app.route("/home")
def display_mesage():
	headline = "Yêu em nhất nhà !"
	return render_template("index1.html", headline=headline)