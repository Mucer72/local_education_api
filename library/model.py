from .extension import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    userName = db.Column(db.String(45), nullable=False)
    firstName = db.Column(db.String(45), nullable=False)
    lastName = db.Column(db.String(45), nullable=False)
    institution = db.Column(db.String(45), nullable=False)
    avtSrc = db.Column(db.String(100), nullable=True)

    user_progress = db.relationship('UserProgress', backref='user', lazy=True)

    def __init__(self, email, password, userName, firstName, lastName, institution, avtSrc):
        self.email = email
        self.password = password
        self.userName = userName
        self.firstName = firstName
        self.lastName = lastName
        self.institution = institution
        self.avtSrc = avtSrc

class UserProgress(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    topicID = db.Column(db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, userID, topicID, score):
        self.userID = userID
        self.topicID = topicID
        self.score = score

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)

    parts = db.relationship('Part', backref='topic', lazy=True)
    types = db.relationship('Type', backref='topic', lazy=True)

    def __init__(self, title, description):
        self.title = title
        self.description = description

class Part(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topicID = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    viewStatus = db.Column(db.Boolean, nullable=False)
    title = db.Column(db.String(100), nullable=False)

    types = db.relationship('Type', backref='part', lazy=True)

    def __init__(self, topicid, viewStatus, title):
        self.topicID = topicid
        self.viewStatus = viewStatus
        self.title = title

class Type(db.Model):
    type = db.Column(db.Integer, primary_key=True)
    partID = db.Column(db.Integer, db.ForeignKey('part.id'), nullable=False)
    topicID = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)
    mediaPath = db.Column(db.JSON, nullable=True)
    content = db.Column(db.JSON, nullable=True)
    viewStatus = db.Column(db.Boolean, nullable=False)

    def __init__(self, type, partid, topicid, mediaPath, content, viewStatus):
        self.type = type
        self.partID = partid
        self.topicID = topicid
        self.mediaPath = mediaPath
        self.content = content
        self.viewStatus = viewStatus