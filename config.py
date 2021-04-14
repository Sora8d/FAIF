import os
from dotenv import load_dotenv

basedir= os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    TESTING= False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never_guess'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or \
    'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS= 1
    MAIL_USERNAME= os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD= os.environ.get('MAIL_PASSWORD')
    ADMINS=['miguelpx2012@gmail.com']

    POSTS_PER_PAGE = 3
