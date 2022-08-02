from sqlalchemy import desc

from flask import Blueprint, render_template, jsonify, url_for, flash, redirect, request as flask_request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required

from application import app
from application.models import *

user = Blueprint('user', __name__)


@user.route('/user/login', methods = ['POST', 'GET'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))

	next_url = flask_request.args.get('next', flask_request.form.get('next', ''))
     
	if flask_request.method == 'POST':
		email = flask_request.form['email']
		user = UserModel.query.filter_by(email = email).first()
		if user is not None and user.check_password(flask_request.form['password']):
			if (not user.roles):
				flash('Your account is disabled', 'error')
			else:
				user.lastlogin = datetime.datetime.utcnow()
				db.session.commit()
				login_user(user)
				flash('You are now logged in')
				if (next_url):
					return redirect(next_url)
				else:
					return redirect(url_for('index'))
		else:
			flash('Wrong email address or password', 'error')
     
	return render_template('user/login.html',
		title='Login',
		menu='login',
		next=next_url)

@user.route('/user/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
     
    if flask_request.method == 'POST':
        email = flask_request.form['email']
        username = flask_request.form['name']
        password = flask_request.form['password']
 
        if UserModel.query.filter_by(email=email).first():
            return ('Email already Present')
	
		# -TODO- register with role = 0 and send confirmation email to move to 1
        user = UserModel(email=email, name=username, roles=1)
        user.set_password(password)
        user.check_gravatar(True)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))

    return render_template('user/register.html',
		title='Register',
		menu='register')

@user.route('/logout')
def logout():
	logout_user()
	flash('You are now logged out')
	return redirect(url_for('index'))