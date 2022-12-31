from db import db 
from flask_login import UserMixin

class Authors(db.Model, UserMixin):
  __tablename__ = 'authors'
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(500), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  posts = db.relationship('Posts', backref='authors', lazy=True)

  # def __repr__(self):
  #   return self.username
