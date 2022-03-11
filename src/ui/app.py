from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import DevelopmentConfig


game_tools = Flask(__name__)
game_tools.secret_key = 'zzz -- 3r 4 gggg4 jjj fw0fj'
game_tools.config.from_object(DevelopmentConfig)

sqldb = SQLAlchemy(game_tools)

login_manager = LoginManager(game_tools)
