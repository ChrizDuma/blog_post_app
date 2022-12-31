from flask import Flask, render_template, abort, session, redirect, request
from flask_admin.contrib.sqla import ModelView #for viewing all data in our table
from models import Posts, Authors
from flask_admin import Admin
# from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from db import db
import os

base_dir = os.path.dirname(os.path.realpath(__file__)) # directory path

app = Flask(__name__)
# configurations
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, 'blog.db')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'my_private_secret-key😉'

# db_configurations
# ------------------------------------------
db.init_app(app)
@app.before_first_request
def create_tables():
  db.create_all()
# ------------------------------------------

# objects
admin = Admin(app) #creating an admin object
# -------------------------------------------------------------------
class SecureModelView(ModelView):
  def is_accessible(self):
    if 'logged_in' in session:
      return True
    else:
      abort(403) #403 -> forbidden access 

admin.add_view(SecureModelView(Posts, db.session)) 
admin.add_view(SecureModelView(Authors, db.session)) 

# -------------------------------------------------------------------
# ----------------------------------------------------------------
# routes
@app.route('/')
def home_page():
  posts = Posts.query.all()
  return render_template('index.html', posts=posts)

@app.route('/about')
def about_page():
  return render_template('about.html')

@app.route('/post/<string:slug>')
def blog_post(slug):
  try:
    post = Posts.query.filter_by(slug=slug).one()
    return render_template('post.html', post=post)
  except sqlalchemy.exc.NoResultFound as e:
    e
    abort(404)
    

@app.route('/contact')
def contact_page():
  return render_template('contact.html')  

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    new_author = Authors(password=password, username=username)
    db.session.add(new_author)
    # db.session.commit()

    if request.form.get('username') == new_author.username and request.form.get('password') == new_author.password:
      db.session.add(new_author)
      db.session.commit()
      session['logged_in'] = True 
      return redirect('/admin')  #redirect('/admin')
    else:
      return render_template('login.html', failed=True) 
  return render_template('login.html') 

@app.route('/logout')
def logout():
  session.clear()
  return redirect('/')
# --------------------------------------------------------------------

if __name__=='__main__':
  app.run(debug=True)