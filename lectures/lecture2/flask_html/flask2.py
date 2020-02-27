from flask import Flask, render_template

import datetime

app = Flask(__name__)


@app.route("/isnewyear")
def isnewyear():
	time = datetime.datetime.now()
	date = time.day
	month = time.month
	flag = True if (date==1 and month==1) else False

	return render_template("index2.html", flag=flag)