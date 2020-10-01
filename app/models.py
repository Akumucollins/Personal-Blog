from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, current_user
from . import login_manager
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    '''
    Role class to define a User's role in the database
    '''

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    user = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class User(UserMixin, db.Model):
    
    '''
    User class to define a user in the database
    '''
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255), unique = True, index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_secure = db.Column(db.String(255))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    posts = db.relationship('Post', backref='username', lazy='dynamic')
 
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password) 
       
    def __repr__(self):
        return f'✍️ {self.username}'
    
    @classmethod
    def check_role(cls,user_id,role_id):
        get_role = User.query.filter_by(id=user_id).filter_by(role_id=role_id).first()
        return get_role

    def save_user(self):
        '''
        Save instance of User model to the session and commit it to the database
        '''
        db.session.add(self)
        db.session.commit()
    
class Post(db.Model):
    '''
    Post class to define a blog post by a user with Writer role
    '''

    __tablename__= 'posts'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255))
    topic = db.Column(db.String(255))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime(250), default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

    def save_post(self):
        '''
        Function that saves a new blog post to the posts table and database
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_posts(id):
        '''
        Function that queries the Posts Table in the database and returns all the information from the Posts Table
        Returns:
            posts : all the information in the posts table
        '''
        posts = Post.query.filter_by(title=title).all()
        return posts

    @classmethod
    def get_posts(cls):
        '''
        Function that queries the Posts Table in the database and returns all the information from the Posts Table
        Returns:
            posts : all the information in the posts table
        '''
        posts = Post.query.order_by(user_id).all()
        return posts    

    def __repr__(self):
        return f"Posts {self.id}','{self.date}')" 
        
class Comment(db.Model):
    '''
    Comment class to define the feedback from users
    '''
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text())
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def save_comment(self):
        '''
        Function that saves a new comment given as feedback to a post
        '''
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comments(cls, post_id):
        '''
        Function that queries the Comments Table in the database and returns only information with the specified post id
        Args:
            post_id : specific post_id
        Returns:
            comments : all the information for comments with the specific post id
        '''
        comments = Comment.query.filter_by(post_id=post_id).all()
        return comments

    @classmethod
    def delete(self):
        '''
        Function that deletes a specific single comment from the comments table and database
        '''
        db.session.delete(self)
        db.session.commit()
    def __repr__(self):
        return f'Comments: {self.comment}'

class Quotes:
    def __init__(self, author, quote):
        self.id = id
        self.author = author
        self.quote = quote
    