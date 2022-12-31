from datetime import datetime
from db import db 

class Posts(db.Model):
  __tablename__ = 'posts'
  id = db.Column(db.Integer(), primary_key=True)
  title = db.Column(db.String(500), nullable=False)
  sub_title = db.Column(db.String(500), nullable=False)
  post_content = db.Column(db.Text(1000),nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
  date_posted = db.Column(db.DateTime(), default=datetime.utcnow())
  slug = db.Column(db.String(500), unique=True, nullable=False)

  def __repr__(self):
    return self.author_id