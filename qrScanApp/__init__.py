from flask import Flask
from config import Define
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

application = Flask(__name__)
application.config.from_object(Define)
storage = SQLAlchemy(application)
migrate = Migrate(application, storage)
login = LoginManager(application)
login.login_view = 'login'

from qrScanApp import routes, models