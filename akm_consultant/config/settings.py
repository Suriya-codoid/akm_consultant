from datetime import timedelta
from decouple import config

DEBUG = True
DEBUG_TB_INTERCEPT_REDIRECTS=False


SECRET_KEY = 'insecurekeyfordev'

# SQLAlchemy.
db_uri = 'mysql+pymysql://root:codoid$15@localhost:3306/akm'
SQLALCHEMY_DATABASE_URI = db_uri
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_RECORD_QUERIES = True
TECH_SUPPORT=config('TECH_SUPPORT', default=list(),cast=lambda x: [s.strip() for s in x.split(',')])

