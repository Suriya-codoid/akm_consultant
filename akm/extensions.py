from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import inspect

debug_toolbar = DebugToolbarExtension()
csrf = CsrfProtect()
db = SQLAlchemy()
login_manager = LoginManager()

class Serializer(object):

    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]
