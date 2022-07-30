from flask import Blueprint, render_template

import datetime

settings = Blueprint('settings', __name__)


@settings.route("/settings/projects")
def projects():
	# List of projects, invitations, join and leave projects
	return render_template("settings_projects.html",
		title="Pacific Data Hub",
		menu="settings_projects",
		now=datetime.datetime.utcnow(),
		js=['dragula.min.js', 'settings_projects.js']
	)

@settings.route("/settings/account")
def account():
	# User account settings, i.e. name, email, password, avatar
	return render_template("settings_account.html",
		title="Pacific Data Hub",
		menu="settings_account",
		now=datetime.datetime.utcnow(),
		js=['settings_account.js']
	)

@settings.route("/settings/preferences")
def preferences():
	# User preferences, i.e. timezone, default view, notifications, outlook sync
	return render_template("settings_preferences.html",
		title="Pacific Data Hub",
		menu="settings_preferences",
		now=datetime.datetime.utcnow(),
		js=['settings_preferences.js']
	)

@settings.route("/settings/users")
def users():
	# User management
	return render_template("settings_users.html",
		title="Pacific Data Hub",
		menu="settings_users",
		now=datetime.datetime.utcnow(),
		js=['settings_users.js']
	)