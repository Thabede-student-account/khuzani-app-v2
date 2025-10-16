from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin
from datetime import datetime
from sqlalchemy import Numeric

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'main.admin_login'

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(128), unique=True, nullable=False)
    title_zu = db.Column(db.String(256), nullable=False)
    title_en = db.Column(db.String(256), nullable=False)
    content_zu = db.Column(db.Text)
    content_en = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title_zu = db.Column(db.String(256), nullable=False)
    title_en = db.Column(db.String(256), nullable=False)
    description_zu = db.Column(db.Text)
    description_en = db.Column(db.Text)
    venue = db.Column(db.String(256))
    date = db.Column(db.DateTime)
    ticket_link = db.Column(db.String(512))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_zu = db.Column(db.String(256), nullable=False)
    name_en = db.Column(db.String(256), nullable=False)
    description_zu = db.Column(db.Text)
    description_en = db.Column(db.Text)
    price = db.Column(Numeric(10,2), nullable=False)
    sku = db.Column(db.String(64))
    image = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    caption_zu = db.Column(db.String(256))
    caption_en = db.Column(db.String(256))
    media_type = db.Column(db.String(32))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
