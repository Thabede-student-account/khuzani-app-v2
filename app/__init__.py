import os
from flask import Flask, session
from .config import Config
from .models import db, migrate, login_manager
from .routes import main_bp
from .payments import payments_bp
from flask_babel import Babel

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        lang = session.get('lang')
        if lang:
            return lang
        return app.config.get('BABEL_DEFAULT_LOCALE', 'zu')

    app.register_blueprint(main_bp)
    app.register_blueprint(payments_bp)
    return app
