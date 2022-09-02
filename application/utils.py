import datetime, pytz
import sqlalchemy as sqa
from application import db
from application.models import *

class utils:

    @staticmethod
    def get_timezones():
        tzgroups = {}
        tzlist = pytz.common_timezones
        for tz in tzlist:
            if '/' in tz:
                tzn = tz.split('/')
                if tzn[0] not in tzgroups:
                    tzgroups[tzn[0]] = []
                tzgroups[tzn[0]].append(tzn[1])
            else:
                tzgroups[tz] = [ tz ]
        return tzgroups

    @staticmethod
    def set_last_login(id):
        usertable = sqa.Table(
            'user', 
            sqa.MetaData(),
            sqa.Column('id', sqa.Integer, primary_key = True), 
            sqa.Column('lastlogin', sqa.DateTime)
        )
        with db.engine.begin() as conn:
            updquery = sqa.update(usertable).where(usertable.c.id==id).values(lastlogin=datetime.datetime.utcnow())
            conn.execute(updquery)

    @staticmethod
    def wrong_project_permission(pid, uid, level):
        if not pid:
            return {'error': 'Project ID is missing'}
        if not uid:
            return {'error': 'User ID is missing'}
        # Check permissions
        asso = ProjectUserModel.query.filter_by(project_id=pid, user_id=uid).first()
        if not asso or asso.role < level:
            return { 'error': 'Insufficient permissions' }
        # all good
        return False

    @staticmethod
    def parse_project(proj, userid):
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
            'mids': [],
            'lists': []
        }
        if proj.status == 2:
            obj['class'] = 'bg-success'
        elif proj.status == 0:
            obj['class'] = 'bg-secondary'
        for asl in proj.lists:
            obj['lists'].append(asl)
        for asm in proj.members:
            obj['mids'].append(asm.member.id)
            obj[f'r{asm.role}'].append(asm.member)
            if asm.role == 2 and asm.member.id == userid:
                obj['isadmin'] = True
        return obj

    @staticmethod
    def parse_projects(plist, userid):
        projects = []
        for proj in plist:
            obj = utils.parse_project(proj, userid)
            projects.append(obj)
        return projects