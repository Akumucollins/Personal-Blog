from flask import render_template,redirect,url_for,abort,request,flash
from flask_login import login_required,current_user
from . import main
from .forms import *
from ..models import *
from .. import db, photos
import markdown2

@main.route('/')
def index():
    """ 
    View root page function that returns index page 
    """
    posts = Post.query.all()
    
    title = 'WELCOME TO PERSONAL BLOGS'
    return render_template('index.html', title = title, posts= posts)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path 
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))
    
    return render_template('profile/update.html',form =form)

@main.route('/post/new', methods = ['GET','POST'])
@login_required
def new_post():
    """
    View Post function that returns the Post page and data
    """
    form = PostForm()

    if form.validate_on_submit():

        topic = form.topic.data
        content= form.content.data
        title=form.title.data

        # Updated Post Instance
        new_post = Post(title=title,topic= topic,content= content,user_id=current_user.id)

        db.session.add(new_post)
        db.session.commit()

        title='New Blog Posted'
        return redirect(url_for('main.index'))

    return render_template('post.html',posts_form= form)