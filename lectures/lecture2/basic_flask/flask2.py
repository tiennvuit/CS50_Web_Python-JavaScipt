from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
	return "Hello World !"


@app.route("/<string:name>")
def hello_name(name: str):
	return f"Hello, {name}"