from flask import Blueprint
from .trades_routes import trade_bp  
from .clear_data_routes import clear_data_bp
from .user_auth_routes import user_auth_bp

def register_routes(app):
    app.register_blueprint(trade_bp, url_prefix='/trades')  
    app.register_blueprint(clear_data_bp, url_prefix='/clear_data') 
    app.register_blueprint(user_auth_bp, url_prefix='/auth') 
