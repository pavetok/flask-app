# -*- coding:utf-8 -*-
from flask.ext.babel import Babel, lazy_gettext
from momentjs import Momentjs
import os
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
from flask.ext.openid import OpenID
from config import basedir
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
mail = Mail(app)
babel = Babel(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = lazy_gettext('Please log in to access this page.')
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models

app.jinja_env.globals['momentjs'] = Momentjs

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT),
                               'no-reply@' + MAIL_SERVER,
                               ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: '
                                                '%(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog startup')

from app.modl.views import modl as modlModule
app.register_blueprint(modlModule)