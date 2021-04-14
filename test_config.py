import os
from dotenv import load_dotenv

basedir= os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Test_Config(object):
    TESTING= True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never_guess'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URL') or \
    'sqlite:///'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 3
