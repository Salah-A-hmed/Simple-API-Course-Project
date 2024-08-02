from app.database import db
from app.models import User
from flask import Blueprint, request, jsonify, abort
import datetime

users_bp = Blueprint('users_v2',__name__)

# Register User
@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        password=data['password'],
        role=data.get('role', 'user'),  # Default to 'user' if not provided
        token=data.get('token'),
        last_request_time=data.get('last_request_time', datetime.datetime.utcnow()),
        request_count=data.get('request_count', 0)
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

#login User
@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        user.generate_token()
        db.session.commit()
        return jsonify({"token":user.token})
    return jsonify({"msg":"Bad username or password"}),401


# Get User details by id
@users_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())



