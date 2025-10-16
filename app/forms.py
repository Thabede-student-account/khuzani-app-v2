from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SubmitField, DecimalField, DateTimeField, FileField
from wtforms.validators import DataRequired, Email, Length
from flask_wtf.file import FileAllowed

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PageForm(FlaskForm):
    slug = StringField('Slug', validators=[DataRequired()])
    title_zu = StringField('Isihloko (isiZulu)', validators=[DataRequired()])
    title_en = StringField('Title (English)', validators=[DataRequired()])
    content_zu = TextAreaField('Okuqukethwe (isiZulu)', validators=[Length(min=0)])
    content_en = TextAreaField('Content (English)', validators=[Length(min=0)])
    submit = SubmitField('Save')

class EventForm(FlaskForm):
    title_zu = StringField('Isihloko (isiZulu)', validators=[DataRequired()])
    title_en = StringField('Title (English)', validators=[DataRequired()])
    description_zu = TextAreaField('Incazelo (isiZulu)')
    description_en = TextAreaField('Description (English)')
    venue = StringField('Venue')
    date = DateTimeField('Date (YYYY-mm-dd HH:MM)', format='%Y-%m-%d %H:%M')
    ticket_link = StringField('Ticket Link')
    submit = SubmitField('Save')

class ProductForm(FlaskForm):
    name_zu = StringField('Igama (isiZulu)', validators=[DataRequired()])
    name_en = StringField('Name (English)', validators=[DataRequired()])
    description_zu = TextAreaField('Incazelo (isiZulu)')
    description_en = TextAreaField('Description (English)')
    price = DecimalField('Price (ZAR)', places=2)
    image = FileField('Image', validators=[FileAllowed(['jpg','jpeg','png','gif'])])
    submit = SubmitField('Save')

class MediaForm(FlaskForm):
    file = FileField('Image / Video', validators=[FileAllowed(['jpg','jpeg','png','gif','mp4','webm'])])
    caption_zu = StringField('Caption (isiZulu)')
    caption_en = StringField('Caption (English)')
    submit = SubmitField('Upload')

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send')
