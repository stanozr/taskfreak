import sys, os, time, json, re
from datetime import datetime, timedelta
# from calendar import monthrange
# from unicodedata import numeric
# from sqlalchemy import desc, or_, and_

# import inquirer

from application import app
# from application.models import TaskModel, TaskLogModel, UserModel
# from application.utils import checkLinkByHeader, notificationTaskDetail

if __name__ == "__main__":
    app.run(host=app.config['FLASK_HOST'], port=app.config['FLASK_PORT'])