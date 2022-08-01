from flask import Flask, g, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user

import datetime

# from datetime import datetime, timedelta
# import time

# import json

app = Flask(__name__)
app.config.from_object('application.config.Config')
app.secret_key = app.config['CKAN_SECRET_KEY']

db = SQLAlchemy(app)

from .models import UserModel

from .views.user import user
app.register_blueprint(user)

from .views.tasks import tasks
app.register_blueprint(tasks)

from .views.settings import settings
app.register_blueprint(settings)

login = LoginManager()
login.init_app(app)
login.login_view = 'user.login'

@login.user_loader
def load_user(id):
    return UserModel.query.get(int(id))

@app.before_request
def before_request():
	g.user = current_user
	g.now = datetime.datetime.utcnow()

@app.template_filter()
def toast_class(ts):
	if ts == 'error':
		return 'text-bg-danger'
	elif ts == 'warning':
		return 'text-bg-warning'
	elif ts == 'success':
		return 'text-bg-success'
	else:
		return 'text-bg-info'

@app.route("/")
def index():
	if not current_user.is_authenticated:
		return redirect(url_for('user.login'))
	else:
		# -TODO- check preferenced view
		return redirect(url_for('tasks.list'))