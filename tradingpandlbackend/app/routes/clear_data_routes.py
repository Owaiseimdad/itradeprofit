from flask import Blueprint, jsonify
from app.models import db, Trade, User

clear_data_bp = Blueprint('clear_data', __name__)

@clear_data_bp.route('/trades', methods=['POST'])
def clear_trade_data():
    try:
        # Clear all records from the Trade and User tables
        db.session.query(Trade).delete()
        db.session.commit()  # Commit changes

        return jsonify({'message': 'All dataof trade table cleared successfully!'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': str(e)}), 500

@clear_data_bp.route('/users-demo', methods=['POST'])
def clear_user_data():
    try:
        db.session.query(User).delete()
        db.session.commit()  # Commit changes

        return jsonify({'message': 'All data for user cleared successfully!'}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({'error': str(e)}), 500
