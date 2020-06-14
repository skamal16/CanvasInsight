from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    reports = db.relationship('Report', backref='user', lazy='dynamic')

    def __repr__(self):
        return 'User: {}'.format(self.username)

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image = db.relationship('Image', backref='report', lazy='dynamic')

    def __repr__(self):
        return 'Report: {}'.format(self.id)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_filename = db.Column(db.String(64), default=None)
    image_url = db.Column(db.String(64), default=None)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))

    def __repr__(self):
        return 'Image: {}'.format(self.id)