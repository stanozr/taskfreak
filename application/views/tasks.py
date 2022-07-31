from flask import Blueprint, render_template
from flask_login import current_user

import datetime

tasks = Blueprint('tasks', __name__)

@tasks.route("/list")
def list():
    return render_template("task_list.html",
		title="Pacific Data Hub",
		menu="list",
		js=['task_list.js']
	)

@tasks.route("/calendar")
def calendar():
	return render_template("task_calendar.html",
		title="Pacific Data Hub",
		menu="calendar",
		js=['calendar.min.js', 'task_calendar.js'],
		css=['calendar.min.css']
	)

@tasks.route("/kanban")
def kanban():
    return render_template("task_kanban.html",
		title="Pacific Data Hub",
		menu="kanban",
		js=['dragula.min.js', 'task_kanban.js']
	)