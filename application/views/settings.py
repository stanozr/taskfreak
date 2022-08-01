import datetime
from sqlalchemy import desc

from flask import Blueprint, render_template, jsonify, request, flash
from flask_login import login_required, current_user

from application import app
from application.models import *

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
	items = UserModel.query.order_by(desc(UserModel.roles), UserModel.name).all()
	return render_template("settings_users.html",
		title="Pacific Data Hub",
		menu="settings_users",
		data=items,
		roles=app.config['USER_ROLES'],
		now=datetime.datetime.utcnow(),
		js=['settings_users.js']
	)

@settings.route("/api/users/load/<id>")
@login_required
def api_user_load(id):
	if current_user.roles < 1:
		return jsonify({'error': 'Action not allowed'})
	item = UserModel.query.filter_by(id=id).first()
	if not item:
		return jsonify({'error': 'User does not exist'}) 
	if current_user.roles <= item.roles:
		return jsonify({'error': 'Action not allowed'})
	return jsonify(item.get_dict())

@settings.route("/api/users/save", methods=['POST'])
@login_required
def api_user_save():
	uid = int(request.form['id']) if request.form.get('id') else False
	uro = int(request.form['roles']) if request.form.get('roles') else 0
	if current_user.roles < 1 or (uid and uid == current_user.id) or (uro > current_user.roles):
		return jsonify({'error': 'Action not allowed'})
	# set user
	item = UserModel()
	if uid:
		item = UserModel.query.filter_by(id=uid).first()
		if not item:
			return jsonify({'error': 'User does not exist'})
	if not uid or current_user.roles > 2:
		# set email only for new users
		# only super admin can change email
		item.email = request.form.get('email','').strip()
	item.name = request.form.get('name','').strip()
	item.roles = uro
	pwd = request.form.get('password','').strip()
	if (pwd):
		# set password only when creating or updating it
		item.set_password(pwd)
	if not item.is_valid():
		return jsonify({'error': 'Missing or invalid fields'})
	if not uid:
		db.session.add(item)
	db.session.commit()
	msg = "User {}".format('Updated' if uid else 'Created')
	flash(msg, 'success')
	return jsonify({'success': msg})
		

@settings.route("/api/users/delete/<int:id>")
@login_required
def api_user_delete(id):
	if current_user.roles < 2:
		return jsonify({'error': 'Insufficient permissions #2'})
	item = UserModel.query.get(id)
	if item:
		db.session.delete(item)
		db.session.commit()
		flash('user deleted', 'success')
		return jsonify({'success': 'User deleted'})
	else: 
		return jsonify({'error': 'User does not exist'})
    # return redirect(url_for('adminUser'))