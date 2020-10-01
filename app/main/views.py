from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required,current_user
from . import main
from ..models import User, Post, Comment
from .forms import UpdateProfile, PostForm, CommentForm
from .. import db, photos
import markdown2
from ..requests import get_quotes

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
        return redirect(url_for('main.all'))

    return render_template('post.html',posts_form= form)

@main.route('/Post/posts', methods=['GET', 'POST'])
@login_required
def posts():
    posts = Post.query.all()
    quote = get_quotes()
    return render_template('posts.html', posts=posts, quote=quote)

@main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    post = Post.query.get_or_404(id)
    post_comments = Comment.query.filter_by(post_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(post_id=id, comment=comment_form.comment.data, author=current_user)
        new_comment.save_comment()
    return render_template('post.html', post=post, post_comments=post_comments, comment_form=comment_form)

@main.route('/post/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    """
    Delete a post from the database
    """
    post = Post.query.get_or_404(id)

    if post.author != current_user:
        abort(403)

    post = Post.query.filter_by(id=id).first()    

    db.session.delete(post)
    db.session.commit()

    flash('Your post has been deleted', 'successfully')
    return redirect(url_for('main.posts'))

@main.route('/Update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_post(id):
    """
    Update or edit a post in the database
    """
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.topic = form.topic.data
        post.content = form.content.data
        post.title =form.title.data

        # Updated bloginstance
        db.session.add(post)
        db.session.commit()

        flash('Your post has been Updated', 'successfully')
        return redirect(url_for('main.posts'))

    elif request.method == 'GET':
       form.topic.data =  post.topic
       form.content.data = post.content
       form.title.data =  post.title
        
    return render_template('update_post.html', form=form)

@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(post_id=id, comment=comment.form.data, author=current_user)
        new_comment.save_comment()
    return render_template('post.html', comment_form=comment_form)  

@main.route('/comment/delete/<int:post_id>' ,methods=['GET', 'POST'])
@login_required
def delete_comment(post_id):

    post = Post.query.filter_by(id=post_id).first()
    comment = Comment.query.filter_by(post_id=post_id).first()

    db.session.delete(comment)
    db.session.commit()

    return redirect(url_for('main.post', comment=comment, post=post, post_id=post_id))      

