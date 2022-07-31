import sys, os, time, json, re
from datetime import datetime, timedelta
# from calendar import monthrange
# from unicodedata import numeric
# from sqlalchemy import desc, or_, and_

# import inquirer

from application import app, db
from application.models import UserModel

if __name__ == "__main__":

    db.create_all()

    # Create default user if user table is empty
    testuser = UserModel.query.first()
    if not testuser:
        user = UserModel(email='admin@test.org', name='Super Admin', roles=3)
        user.set_password('admin')
        db.session.add(user)
        db.session.commit()

    app.run(host=app.config['FLASK_HOST'], port=app.config['FLASK_PORT'])