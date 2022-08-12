from sqlalchemy import desc

from flask import Blueprint, render_template, jsonify, request, url_for, flash, g
from flask_login import login_required, current_user

from application import app
from application.models import *
from application.utils import utils

projects = Blueprint('projects', __name__)

@projects.before_request
@login_required
def login_required_for_all_request():    
    pass  

@projects.route("/projects")
def list():
	# List of projects, invitations, join and leave projects
	plist = ProjectModel.query \
		.join(ProjectUserModel) \
	 	.filter(ProjectModel.status > 0, ProjectUserModel.user_id == current_user.id) \
	 	.order_by(ProjectModel.title).all()
	projects = []
	for proj in plist:
		obj = {
			'id': proj.id,
			'title': proj.title,
			'start': proj.start,
			'deadline': proj.deadline,
			'budget': proj.budget,
			'status': proj.status,
			'isadmin': False,
			'r2': [],
			'r1': [],
			'r0': [],
			'lists': []
		}
		for asl in proj.lists:
			obj['lists'].append(asl)
		for asm in proj.members:
			obj[f'r{asm.role}'].append(asm.member)
			if asm.role == 2 and asm.member.id == current_user.id:
				obj['isadmin'] = True
		projects.append(obj)
	# prepare view
	g.jscript.append(url_for('static', filename='js/dragula.min.js'))
	g.jscript.append(url_for('static', filename='js/projects.js'))
	return render_template("projects.html",
		title="Pacific Data Hub",
		projects=projects,
		menu="projects_list"
	)

@projects.route("/api/project/load/<id>")
@projects.route("/api/project/load/<id>/<mode>")
def api_project_load(id, mode="data"):
	if current_user.role < 1:
		return jsonify({'error': 'Action not allowed'})
	item = ProjectModel.query.filter_by(id=id).first()
	if not item:
		return jsonify({'error': 'Project does not exist'}) 
	return jsonify(item.get_dict(mode))

@projects.route("/api/project/save", methods=['POST'])
def api_project_save():
	pid = int(request.form['id']) if request.form.get('id') else False
	# set user
	item = ProjectModel()
	if pid:
		item = ProjectModel.query.filter_by(id=pid).first()
		if not item:
			return jsonify({'error': 'Project does not exist'})
	
	item.title = request.form.get('title','').strip()
	item.description = request.form.get('description','')
	item.start = request.form.get('start') or None
	item.deadline = request.form.get('deadline') or None
	item.budget = request.form.get('budget') or None # TODO check float
	item.status = request.form.get('status', 0)
	is_valid = item.is_valid()
	if is_valid != True:
		return jsonify({'error': list(is_valid.values())})
	if not pid:
		asso = ProjectUserModel()
		asso.member = current_user
		asso.project = item
		asso.role = 2 # admin
		db.session.add(asso)
	db.session.commit()
	msg = "Project {}".format('Updated' if pid else 'Created')
	flash(msg, 'success')
	return jsonify({
		'success': msg,
		'pid': item.id
	})
