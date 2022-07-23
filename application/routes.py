from flask import render_template, jsonify, send_from_directory, url_for, flash, redirect, safe_join, request as flask_request
# from flask_login import LoginManager, current_user, login_user, logout_user, login_required

import json
# from sqlalchemy import desc

from application import app
# from application.utils import tasksList, getColorShades, dictToList
# from application.data import DataReaderClass
# from application.models import *

import datetime
# from calendar import monthrange

# ------------------------------------- PUBLIC PAGES

@app.route("/")
def index():
	return redirect(url_for('list'))

@app.route("/list")
def list():
    return render_template("task_list.html",
		title="Pacific Data Hub",
		menu="list",
		now=datetime.datetime.utcnow()
	)

@app.route("/calendar")
def calendar():
	return render_template("task_calendar.html",
		title="Pacific Data Hub",
		menu="calendar",
		now=datetime.datetime.utcnow(),
		js=['calendar.min.js', 'task_calendar.js'],
		css=['calendar.min.css']
	)