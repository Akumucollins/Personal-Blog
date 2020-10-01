from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import Required


class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about youself.',validators = [Required()])
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    title = StringField('Blog Title')
    topic = StringField('Blog Topic')
    content = TextAreaField('Blog Content')
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Write a comment', validators=[Required()])
    submit = SubmitField('Comment')    