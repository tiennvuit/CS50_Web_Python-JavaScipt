from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
	return "Hello World!"


@app.route("/tiennv")
def hello_tien():
	return "Hello, Tiến Nguyễn !"