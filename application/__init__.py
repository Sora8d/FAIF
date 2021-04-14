from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
#This one to send error messages to gmail
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

#This one deals with mail (not with mail logs)
from flask_mail import Mail

#To deal with dates
from flask_moment import Moment

#Now to start messing around with SocketIO
import socketio

#To import errors
#Creating the Blueint for errors

sio = socketio.Server()
mail= Mail()

db= SQLAlchemy()
migrate= Migrate()

login = LoginManager()
login.login_view= 'auth.loginn'

moment= Moment()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    login.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)

#    socketio.init_app(app)

    from application.main import bp as main_bp
    app.register_blueprint(main_bp)
    from application.errors import bp as errors_bp
    app.register_blueprint(errors_bp)
    from application.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from application.messages import bp as msg_bp
    app.register_blueprint(msg_bp)
    from application.socketo import bp as sio_bp
    app.register_blueprint(sio_bp)


    if not app.debug and not app.config['TESTING']:
    #Mail log to send errors ocurred in the server
        if app.config['MAIL_SERVER']:
            auth= None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure= None
            if app.config['MAIL_USE_TLS']:
                secure=()
            mail_handler= SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@'+app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Ya Server',
            credentials=auth, secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)
    #This is a files log.
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/yaserver.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Ya Server startup')

    return app
from application import models
