from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

from datetime import datetime, timedelta
import time

import json
 
app = Flask(__name__)
app.config.from_object('application.config.Config')
app.secret_key = app.config['CKAN_SECRET_KEY']

# db = SQLAlchemy(app)

# login = LoginManager()
# login.init_app(app)
# login.login_view = 'login'

from application import routes # , utils, models