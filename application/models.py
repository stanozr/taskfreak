import datetime, requests, hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from application import db

class UserModel(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(128))
    thumbnail = db.Column(db.String(512))
    timezone = db.Column(db.String(64), default='UTC')
    preferences = db.Column(db.String(64))
    creation = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    update = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable = False)
    lastlogin = db.Column(db.DateTime)
    roles = db.Column(db.Integer) # 0 = disabled, 1 = user, 2 = manager, 3 = admin, 4 = super admin

    def set_password(self,password):
        self.password = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password, password)

    def check_gravatar(self, set=False):
        if not self.email:
            return False
        m = hashlib.md5()
        m.update(self.email.encode('ascii', errors='ignore'))
        grav_url = "http://www.gravatar.com/avatar/" + m.hexdigest()
        r = requests.get(grav_url + "?d=404")
        if r.ok:
            if set:
                self.thumbnail = grav_url
            return grav_url
        else:
            return False

    def avatar(self):
        srn = ''
        arn = self.name.split(' ')[0:2]
        for en in arn:
            srn += en[0].upper()
        if self.thumbnail:
            # return '<img src="'+self.thumbnail+'" class="rounded-circle" />'
            return '<span class="avatar-img rounded-circle" style="background-image:url({})">{}</span>'.format(self.thumbnail, srn)
        else:
            return '<span class="avatar-srn rounded-circle">{}</span>'.format(srn)

    def is_valid(self):
        if self.email and '@' in self.email and self.name and self.password:
            return True
        else:
            return False

    def get_dict(self):
        res = {}
        columns = self.__table__.columns.keys()
        for key in columns:
            if key != 'password':
                res[key] = getattr(self, key)
        return res

    