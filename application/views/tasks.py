from flask import Blueprint, render_template, jsonify, redirect, request, url_for, flash, g
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
def dalist(pid=None, lid=None):
    # projects
    g.jscript.append(url_for('static', filename='js/tasks.js'))
    g.jscript.append(url_for('static', filename='js/tasks_list.js'))
    return render_template("task_list.html",
        title="Pacific Data Hub",
        projects = utils.load_projects(current_user),
        opened_project=pid,
        opened_list=lid,
        menu="list"
    )

@tasks.route("/calendar")
def dacalendar():
    g.css.append(url_for('static', filename='css/calendar.min.css'))
    g.jscript.append(url_for('static', filename='js/calendar.min.js'))
    g.jscript.append(url_for('static', filename='js/tasks.js'))
    g.jscript.append(url_for('static', filename='js/tasks_calendar.js'))
    return render_template("task_calendar.html",
        title="Pacific Data Hub",
        projects = utils.load_projects(current_user),
        menu="calendar"
    )

@tasks.route("/kanban")
def dakanban():
    g.jscript.append(url_for('static', filename='js/dragula.min.js'))
    g.jscript.append(url_for('static', filename='js/tasks.js'))
    g.jscript.append(url_for('static', filename='js/tasks_kanban.js'))
    return render_template("task_kanban.html",
        title="Pacific Data Hub",
        projects = utils.load_projects(current_user),
        menu="kanban"
    )

@tasks.route("/api/task/load/<id>")
@tasks.route("/api/task/load/<id>/<mode>")
def api_load(id, mode="data"):
    if current_user.role < 1:
        return jsonify({'error': 'Action not allowed'})
    item = TaskModel.query.filter_by(id=id).first()
    if not item:
        return jsonify({'error': 'Project does not exist'})
    if mode == 'data':
        return jsonify(item.get_dict())
    else:
        return jsonify(item.get_html())

@tasks.route('/api/task/save', methods=['POST'])
def api_save():
    tid = int(request.form['id']) if request.form.get('id') else False
    # init task
    item = TaskModel()
    if tid:
        item = TaskModel.query.filter_by(id=tid).first()
        if not item:
            return jsonify({'error': 'Task does not exist'})
        err = utils.wrong_project_permission(item.project_id, current_user.id, 1)
        if err:
            return jsonify(err)
    # set properties
    item.title = request.form.get('title','').strip()
    item.project_id = request.form.get('project_id', 0)
    item.description = request.form.get('description','')
    item.priority = request.form.get('priotity', 0)
    item.setDate('start',request.form.get('start') or None)
    item.setDate('deadline', request.form.get('deadline') or None)
    item.estimate = request.form.get('estimate') or None
    item.position = request.form.get('position', 0)
    item.status = request.form.get('status', 0)
    # check
    is_valid = item.is_valid()
    if is_valid != True:
        return jsonify({'error': list(is_valid.values())})
    # add task history
    msg = "Task {}".format('Updated' if tid else 'Created')
    activity = TaskActivityModel()
    activity.user = current_user
    activity.task = item
    activity.actype = 1 # history
    activity.comment = msg
    db.session.add(activity)
    # save in DB
    db.session.commit()
    # report to user
    flash(msg, 'success')
    return jsonify({
        'success': msg,
        'id': item.id
    })