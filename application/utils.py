import datetime, pytz
import sqlalchemy as sqa
from application import db

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