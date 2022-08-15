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
def project_list():
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
            'start': proj.getDate('start'),
            'deadline': proj.getDate('deadline'),
            'budget': proj.budget,
            'status': proj.status,
            'class': 'bg-header',
            'isadmin': False,
            'r2': [],
            'r1': [],
            'r0': [],
            'lists': []
        }
        if proj.status == 2:
            obj['class'] = 'bg-success'
        elif proj.status == 0:
            obj['class'] = 'bg-secondary'
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
    item.setDate('start',request.form.get('start') or None)
    item.setDate('deadline', request.form.get('deadline') or None)
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

@projects.route("/api/project/lists/save", methods=['POST'])
def api_project_lists_save():
    if not request.form.get('pid'):
        return jsonify({
            'error': 'Project ID is missing'
        })
    pid = int(request.form['pid'])
    # -TODO- Load project and check admin rights
    proj = ProjectModel.query.get(pid)

    # Create list item
    if (request.form.get('newitem')):
        item = ListModel(
            project_id = pid,
            title=request.form['newitem'],
            position = proj.get_next_list_position(),
            status = 1
        )
        db.session.add(item)
        db.session.commit()
        return jsonify({
            'success': "New list created",
            'pid': pid,
            'lid': item.id,
            'position': item.position
        })
    else:
        # save list items
        items = request.form.to_dict()
        pos = 0
        for idx in items:
            if 'item_' in idx:
                lid = int(idx[5:])
                item = ListModel.query.get(lid)
                if items[idx]:
                    # TODO delete lists with empty names?
                    item.title = items[idx]
                item.project_id = pid
                item.position = pos
                pos = pos+1
        db.session.commit()
        msg = 'List item saved!'
        return jsonify({
            'success': msg,
            'noreload': True,
            'pid': pid
        })

@projects.route("/api/project/lists/del/<int:id>", methods=['GET','POST'])
def api_project_lists_del(id):
    # 1. load list
    print(f'Loading #{id}')
    # 2. Load project and check admin rights
    # 3. load tasks and check list is empty
    # 4. delete list
    # 5. frontend feedback
    return jsonify({
        'success': 'List deleted!'
    })