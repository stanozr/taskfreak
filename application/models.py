import datetime, json, requests, hashlib
from operator import truediv
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from application import app, db

class UserModel(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    name = db.Column(db.String(128))
    thumbnail = db.Column(db.String(512))
    timezone = db.Column(db.String(64), default='UTC')
    preferences = db.Column(db.Text)
    creation = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    lastupdate = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable = False)
    lastlogin = db.Column(db.DateTime)
    role = db.Column(db.SmallInteger) # 0 = disabled, 1 = user, 2 = manager, 3 = admin, 4 = super admin

    projects = db.relationship("ProjectUserModel", back_populates="member")
    
    def get_preferences(self):
        prefs = {}
        try:
            if self.preferences:
                prefs = json.loads(self.preferences)
        except:
            pass
        return prefs
    
    def get_preference(self, key, default=None):
        return self.get_preferences().get(key, default)
        
    def set_preference(self, key, value):
        prefs = self.get_preferences()
        prefs[key] = value
        self.preferences = json.dumps(prefs)

    def set_password(self, password):
        self.password = generate_password_hash(password)
     
    def check_password(self, password):
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

    def avatar(self, xtra=False):
        srn = ''
        arn = self.name.split(' ')[0:2]
        for en in arn:
            srn += en[0].upper()
        lbl = self.name
        if xtra:
            lbl = f"{lbl} ({xtra})"
        if self.thumbnail:
            # return '<img src="'+self.thumbnail+'" class="rounded-circle" />'
            return '<span class="avatar-img rounded-circle" title="{}" style="background-image:url({})">{}</span>'.format(lbl, self.thumbnail, srn)
        else:
            return '<span class="avatar-srn rounded-circle" title="{}">{}</span>'.format(lbl, srn)

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

class ProjectModel(db.Model):
    __tablename__ = "project"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    description = db.Column(db.Text)
    start = db.Column(db.Date, nullable = True)
    deadline = db.Column(db.Date, nullable = True)
    creation = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    lastupdate = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable = False)
    budget = db.Column(db.Float)
    status = db.Column(db.SmallInteger) # 0 = closed, 1 = open (private), 2 = open (public)

    lists = db.relationship('ListModel', order_by='ListModel.position', back_populates='parent', cascade='all, delete-orphan')
    members = db.relationship('ProjectUserModel', order_by='desc(ProjectUserModel.role)', back_populates='project')

    def getDate(self, key):
        value = self.__getattribute__(key)
        if value:
            return value.strftime('%d/%m/%Y')
        else:
            return None

    def setDate(self, key, value):
        if value:
            try:
                self.__setattr__(key, datetime.datetime.strptime(value, '%d/%m/%Y'));
            except:
                pass
        else:
            self.__setattr__(key, None)

    def get_next_list_position(self):
        # SELECT MAX(position)+1 FROM public.list WHERE project_id=ID
        pos = db.session.query(db.func.max(ListModel.position)).filter_by(project_id=self.id).first()[0] or -1
        return pos + 1

    def is_valid(self):
        if self.title:
            item = ProjectModel.query.filter_by(title=self.title).first()
            if item and item.id != self.id:
                return {'title': 'Title already exists'}
            else:
                return True
        return {'title': 'Title is compulsory'}
            

    def get_dict(self, mode="data"):
        res = {}
        columns = self.__table__.columns.keys()
        for key in columns:
            val = getattr(self, key);
            if val:
                if mode == 'html':
                    if key == 'description':
                        # TODO markdown
                        val = '<br />\n'.join(val.split('\n')) 
                    elif key == 'status':
                        val = app.config['PROJECT_STATUS'][val]
                if key == 'start' or key == 'deadline':
                    val = val.strftime('%d/%m/%Y')
            elif mode == 'html':
                val = '-'
            res[key] = val
        return res

class ListModel(db.Model):
    __tablename__ = "list"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"), primary_key=False)
    title = db.Column(db.String(255), unique=True)
    position = db.Column(db.SmallInteger)
    creation = db.Column(db.DateTime, nullable = False, default=datetime.datetime.utcnow)
    lastupdate = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow, nullable = False)
    status = db.Column(db.SmallInteger) # 0 = closed, 1 = open (all), 2 = open (admin only)

    parent = db.relationship('ProjectModel', back_populates='lists')

    def is_valid(self):
        if self.name:
            return True
        else:
            return False

    def get_dict(self):
        res = {}
        columns = self.__table__.columns.keys()
        for key in columns:
            res[key] = getattr(self, key)
        return res

class ProjectUserModel(db.Model):
    __tablename__ = 'projuser'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    project_id = db.Column(db.ForeignKey('project.id'), primary_key=True)
    role = db.Column(db.SmallInteger)
        # 0: Observer (can view and comment)
        # 1: Member (can create/edit/move tasks and lists)
        # 2: Admin (can manage members)

    member = db.relationship('UserModel', back_populates='projects')
    project = db.relationship('ProjectModel', back_populates='members')