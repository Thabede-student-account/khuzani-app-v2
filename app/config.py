import os
from dotenv import load_dotenv
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '..', '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'change-this-key')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, '..', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', MAIL_USERNAME)
    BOOKING_EMAIL = os.environ.get('BOOKING_EMAIL', MAIL_USERNAME)

    PAYFAST_MERCHANT_ID = os.environ.get('PAYFAST_MERCHANT_ID')
    PAYFAST_MERCHANT_KEY = os.environ.get('PAYFAST_MERCHANT_KEY')
    PAYFAST_TEST = os.environ.get('PAYFAST_TEST', 'True') == 'True'
    PAYFAST_RETURN_URL = os.environ.get('PAYFAST_RETURN_URL')
    PAYFAST_CANCEL_URL = os.environ.get('PAYFAST_CANCEL_URL')
    PAYFAST_NOTIFY_URL = os.environ.get('PAYFAST_NOTIFY_URL')

    PAYPAL_CLIENT_ID = os.environ.get('PAYPAL_CLIENT_ID')
    PAYPAL_SECRET = os.environ.get('PAYPAL_SECRET')
    PAYPAL_ENV = os.environ.get('PAYPAL_ENV', 'sandbox')

    BABEL_DEFAULT_LOCALE = 'zu'
    BABEL_SUPPORTED_LOCALES = ['zu', 'en']
