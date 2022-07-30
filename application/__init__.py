from flask import Flask, url_for, flash, redirect
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# from datetime import datetime, timedelta
# import time

# import json

app = Flask(__name__)
app.config.from_object('application.config.Config')
app.secret_key = app.config['CKAN_SECRET_KEY']

from .views.tasks import tasks
app.register_blueprint(tasks)

from .views.settings import settings
app.register_blueprint(settings)

# db = SQLAlchemy(app)

# login = LoginManager()
# login.init_app(app)
# login.login_view = 'login'

@app.route("/")
def index():
	return redirect(url_for('tasks.list'))