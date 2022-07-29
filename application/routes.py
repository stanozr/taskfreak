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
		now=datetime.datetime.utcnow(),
		js=['task_list.js']
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

@app.route("/kanban")
def kanban():
    return render_template("task_kanban.html",
		title="Pacific Data Hub",
		menu="kanban",
		now=datetime.datetime.utcnow(),
		js=['dragula.min.js', 'task_kanban.js']
	)

@app.route("/settings/projects")
def settings_projects():
	# List of projects, invitations, join and leave projects
	return render_template("settings_projects.html",
		title="Pacific Data Hub",
		menu="settings_projects",
		now=datetime.datetime.utcnow(),
		js=['dragula.min.js', 'settings_projects.js']
	)

@app.route("/settings/account")
def settings_account():
	# User account settings, i.e. name, email, password, avatar
	return render_template("settings_account.html",
		title="Pacific Data Hub",
		menu="settings_account",
		now=datetime.datetime.utcnow(),
		js=['settings_account.js']
	)

@app.route("/settings/preferences")
def settings_preferences():
	# User preferences, i.e. timezone, default view, notifications, outlook sync
	return render_template("settings_preferences.html",
		title="Pacific Data Hub",
		menu="settings_preferences",
		now=datetime.datetime.utcnow(),
		js=['settings_preferences.js']
	)

@app.route("/settings/users")
def settings_users():
	# User management
	return render_template("settings_users.html",
		title="Pacific Data Hub",
		menu="settings_users",
		now=datetime.datetime.utcnow(),
		js=['settings_users.js']
	)