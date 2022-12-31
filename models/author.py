from db import db 

class Authors(db.Model):
  __tablename__ = 'authors'
  id = db.Column(db.Integer(), primary_key=True)
  username = db.Column(db.String(500), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  posts = db.relationship('Posts', backref='authors', lazy=True)

  def __repr__(self):
    return self.username
