from flask import Blueprint, render_template, url_for, g
from flask_login import current_user, login_required
from application.models import *
from application.utils import utils

import datetime

tasks = Blueprint('tasks', __name__)

@tasks.before_request
@login_required
def login_required_for_all_request():    
    pass  

@tasks.route("/list")
@tasks.route("/list/<int:pid>")
@tasks.route("/list/<int:pid>/<int:lid>")
def list(pid=None, lid=None):
    # projects
    g.jscript.append(url_for('static', filename='js/task_list.js'))
    return render_template("task_list.html",
        title="Pacific Data Hub",
        projects = utils.load_projects(current_user),
        opened_project=pid,
        opened_list=lid,
        menu="list"
    )

@tasks.route("/calendar")
def calendar():
    g.css.append(url_for('static', filename='css/calendar.min.css'))
    g.jscript.append(url_for('static', filename='js/calendar.min.js'))
    g.jscript.append(url_for('static', filename='js/task_calendar.js'))
    return render_template("task_calendar.html",
        title="Pacific Data Hub",
        projects = utils.load_projects(current_user),
        menu="calendar"
    )

@tasks.route("/kanban")
def kanban():
    g.jscript.append(url_for('static', filename='js/dragula.min.js'))
    g.jscript.append(url_for('static', filename='js/task_kanban.js'))
    return render_template("task_kanban.html",
        title="Pacific Data Hub",
        projects = utils.load_projects(current_user),
        menu="kanban"
    )