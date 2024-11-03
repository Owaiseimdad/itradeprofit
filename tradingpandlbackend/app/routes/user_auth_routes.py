from flask import Blueprint, request, jsonify
from app.models import db, User 
from flask_cors import CORS
import os

user_auth_bp = Blueprint('user_auth', __name__)
CORS(user_auth_bp, origins=["http://localhost:3001"])

SECRET_STRING = os.getenv('SECRET_STRING')

@user_auth_bp.route('/', methods=['GET'])
def health_check():
    return jsonify({'message': "user api all good"}), 200 

@user_auth_bp.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    print(data)
    user_id = data.get('uid')  # UID from Firebase
    email = data.get('email')
    username = data.get('username')
    user = User.query.filter_by(uuid=user_id).first() 

    if not user_id:
        return jsonify({'error': 'Firebase UID is required.'}), 400
    
    if username != user.username:
        print(data['username'])
        user.username = data['username']
        db.session.commit()

    existing_user = User.query.filter_by(uuid=user_id).first()
    if existing_user:
        return jsonify({'message': 'User already exists.'}), 200

    new_user = User(uuid=user_id, email=email, username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User added successfully.'}), 201


@user_auth_bp.route('/user/<uuid>', methods=['GET'])
def get_user(uuid):
    user = User.query.filter_by(uuid=uuid).first()
    if user:
        return jsonify({'exists': True, 'user': {'uuid': user.uuid, 'email': user.email, 'username': user.username}}), 200
    else:
        return jsonify({'exists': False}), 404


@user_auth_bp.route('/all_users', methods=['POST'])
def get_all_users():
    data = request.json
    secret = data.get('secret')

    if secret != SECRET_STRING:
        return jsonify({'error': 'Unauthorized access.'}), 403

    users = User.query.all()
    users_list = [
        {
            'id': user.id,
            'uuid': user.uuid,
            'email': user.email,
            'username': user.username,
            'created_at': user.created_at
        } for user in users
    ]
    return jsonify(users_list), 200