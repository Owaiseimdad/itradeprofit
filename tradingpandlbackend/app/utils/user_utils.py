from app.models import User
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def user_exists(user_id):
    """Check if a user exists by user_id."""
    user = User.query.filter_by(uuid=user_id).first() 
    return user is not None  
