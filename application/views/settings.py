import datetime, pytz
from sqlalchemy import desc

from flask import Blueprint, render_template, jsonify, request, flash
from flask_login import login_required, current_user

from application import app
from application.models import *
from application.utils import utils

settings = Blueprint('settings', __name__)

@settings.before_request
@login_required
def login_required_for_all_request():    
    pass  

@settings.route("/settings/projects")
def projects():
	# List of projects, invitations, join and leave projects
	return render_template("settings_projects.html",
		title="Pacific Data Hub",
		menu="settings_projects",
		js=['dragula.min.js', 'settings_projects.js']
	)

@settings.route("/settings/account")
def account():
	# User account settings, i.e. name, email, password, avatar
	# item = UserModel.query.get(current_uset)
	return render_template("settings_account.html",
		title="Pacific Data Hub",
		menu="settings_account",
		data=current_user,
		timezones=utils.get_timezones(),
		js=['settings_account.js']
	)

@settings.route("/settings/preferences")
def preferences():
	# User preferences, i.e. timezone, default view, notifications, outlook sync
	opts = {
		'default_views': app.config['TASK_VIEWS']
	}
	return render_template("settings_preferences.html",
		title="Pacific Data Hub",
		menu="settings_preferences",
		data=current_user.get_preferences(),
		options = opts,
		js=['settings_preferences.js']
	)

@settings.route("/api/preferences/save", methods=['POST'])
def api_preferences_save():
	uid = int(request.form['id']) if request.form.get('id') else current_user.id
	if uid != current_user.id and current_user.roles < 3:
		return jsonify({'error': 'You must be admin to edit users'})
	item = UserModel.query.filter_by(id=uid).first()
	if not item:
		return jsonify({'error': 'User does not exist'})
	item.set_preference('default_view', request.form.get('default_view', 'list'))
	item.set_preference('notif_instant', request.form.get('notif_instant', False))
	item.set_preference('notif_daily', request.form.get('notif_daily', False))
	db.session.commit()
	msg = "User preferences saved"
	return jsonify({'success': msg})

@settings.route("/settings/users")
def users():
	# User management
	items = UserModel.query.filter(UserModel.roles > 0).order_by(desc(UserModel.roles), UserModel.name).all()
	return render_template("settings_users.html",
		title="Pacific Data Hub",
		menu="settings_users",
		data=items,
		roles=app.config['USER_ROLES'],
		timezones=utils.get_timezones(),
		js=['settings_users.js']
	)

@settings.route("/api/users/load/<id>")
def api_user_load(id):
	if current_user.roles < 2:
		return jsonify({'error': 'Action not allowed'})
	item = UserModel.query.filter_by(id=id).first()
	if not item:
		return jsonify({'error': 'User does not exist'}) 
	if current_user.roles <= item.roles:
		return jsonify({'error': 'Action not allowed'})
	if not item.timezone:
		item.timezone = 'UTC'
	return jsonify(item.get_dict())

@settings.route("/api/users/save", methods=['POST'])
def api_user_save():
	uid = int(request.form['id']) if request.form.get('id') else False
	uro = int(request.form['roles']) if request.form.get('roles') else 0
	if (uid != current_user.id and uro > current_user.roles):
		# trying to raise user to a higher level than ourself
		return jsonify({'error': 'Action not allowed'})
	# set user
	item = UserModel()
	if uid:
		item = UserModel.query.filter_by(id=uid).first()
		if not item:
			return jsonify({'error': 'User does not exist'})
		elif uid != current_user.id:
			if current_user.roles < 3:
				return jsonify({'error': 'You must be admin to edit users'})
			if current_user.roles <= item.roles:
				return jsonify({'error': 'Can not edit user with a higher role'})
	elif current_user.roles < 3:
		return jsonify({'error': 'You must be admin to create users'})
		
	item.name = request.form.get('name','').strip()
	item.timezone = request.form.get('timezone','UTC')
	if not uid or (uid != current_user.id and current_user.roles > 3):
		# set email only for new users
		# only super admin can change email (for now)
		item.email = request.form.get('email','').strip()
	if (uid and uid == current_user.id):
		# user is updating itself
		item.thumbnail = request.form.get('thumbnail', '')
	else:
		# admin is updating another user
		item.roles = uro
	# check if password is getting updated
	pwd = request.form.get('password','').strip()
	if (pwd):
		# set password only when creating or updating it
		# -TODO- check if the password is secure enough (within set_password method)
		item.set_password(pwd)
	if not item.is_valid():
		return jsonify({'error': 'Missing or invalid fields'})
	if not uid:
		db.session.add(item)
	db.session.commit()
	msg = "User {}".format('Updated' if uid else 'Created')
	flash(msg, 'success')
	return jsonify({
		'success': msg, 
		'avatar': item.avatar()
	})


@settings.route("/api/users/delete/<int:id>", methods=['POST'])
def api_user_delete(id):
	# id = int(request.form['id']) if request.form.get('id') else False
	if not id:
		return jsonify({'error': 'User not specified'})
	if current_user.roles < 3:
		return jsonify({'error': 'Insufficient permissions #2'})
	item = UserModel.query.get(id)
	if item:
		# delete if no task, no comment, nothing
		# db.session.delete(item)
		# else disable it
		item.roles = 0
		db.session.commit()
		flash('User account has been disabled', 'success')
		return jsonify({'success': 'User disabled'})
	else: 
		return jsonify({'error': 'User does not exist'})
    # return redirect(url_for('adminUser'))