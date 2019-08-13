from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from .blueprints.page import page
from .blueprints.user import user
from .blueprints.user.models import User
from .extensions import (
    debug_toolbar,
    csrf,
    db,
    login_manager
)

def create_app(settings_override=None):
    """
    Create a Flask application using the app factory pattern.

    :param settings_override: Override settings
    :return: Flask app
    """
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)



    if settings_override:
        app.config.update(settings_override)

    app.register_blueprint(page)
    app.register_blueprint(user)
    extensions(app)
    authentication(app, User)

    return app


def extensions(app):
    """
    Register 0 or more extensions (mutates the app passed in).

    :param app: Flask application instance
    :return: None
    """
    debug_toolbar.init_app(app)
    csrf.init_app(app)
    db.init_app(app)

    login_manager.init_app(app)

    return None


def authentication(app, user_model):
    """
    Initialize the Flask-Login extension (mutates the app passed in).

    :param app: Flask application instance
    :param user_model: Model that contains the authentication information
    :type user_model: SQLAlchemy model
    :return: None
    """
    login_manager.login_view = 'user.signin'

    @login_manager.user_loader
    def load_user(uid):
        return user_model.query.get(uid)


