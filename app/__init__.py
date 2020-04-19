from flask import Flask
from flask import request, current_app
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_wtf.csrf import CSRFProtect
from flask_dropzone import Dropzone

import logging
import os, sys
from logging.handlers import SMTPHandler, RotatingFileHandler


# application factory functions:
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db, compare_type=True)
login = LoginManager(app)
login.login_view = 'login'
dropzone = Dropzone(app)

csrf = CSRFProtect(app)

from app import routes, models