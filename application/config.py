import os
from dotenv import load_dotenv

class Config(object):

    load_dotenv('.flaskenv') # needed when running CLI

    CKAN_SECRET_KEY = os.environ.get("CKAN_SECRET_KEY") or b'taskfreak-python-ver1.0'
    
    CKAN_DATA_FOLDER = os.environ.get("CKAN_DATA_FOLDER") or "_data"

    FLASK_HOST = os.environ.get("FLASK_HOST") or '127.0.0.1'
    FLASK_PORT = os.environ.get("FLASK_PORT") or 5001

    APP_URL = os.environ.get('APP_URL') or 'http://127.0.0.1:5001'

    SQLALCHEMY_DATABASE_URI = 'postgresql://stan:Stqn56@localhost:5432/taskfreak'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    TASK_VIEWS = {
        'list': 'List',
        'calendar': 'Calendar',
        'kanban': 'Kanban'
    }

    USER_ROLES = {
        1: "User",
        2: "Manager",
        3: "Administrator",
        4: "Super Admin"
    }