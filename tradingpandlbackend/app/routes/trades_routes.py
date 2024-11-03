from flask import Blueprint, request, jsonify
from flask_cors import CORS
from app.models import db
from app.services.trade_services import process_trades, serialize_all_trade
from app.models import Trade
from app.utils.user_utils import user_exists 

trade_bp = Blueprint('trade', __name__)
CORS(trade_bp, origins=["http://localhost:3001"])

@trade_bp.route('/', methods=['GET'])
def health_check():
    return jsonify({'message': "All good"}), 200 

@trade_bp.route('/upload', methods=['POST'])
def upload_trades():
    user_id = request.form.get('uid')
    if not (user_id):
        return jsonify({'error': 'User not found.'}), 404
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    print(file)
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400

    try:
        pnl_result_serialized = process_trades(file, user_id)
        return jsonify({
            'message': 'File uploaded successfully!',
            'P&L': pnl_result_serialized['PnL'],
            'P&L_plain': pnl_result_serialized['Pnl_no_date']
        }), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to process trades: {str(e)}'}), 500

@trade_bp.route('/all_trades', methods=['GET'])
def get_trades():
    trades = Trade.query.all()
    trades_list = [serialize_all_trade(t) for t in trades]
    return jsonify(trades_list), 200
