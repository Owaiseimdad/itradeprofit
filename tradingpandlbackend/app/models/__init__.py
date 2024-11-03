from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_model import User
from .trade_model import Trade