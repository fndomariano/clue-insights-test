from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from src import bcrypt
from src.models.user import User


bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password_hash, data['password']):
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={"sub": str(user.id)}
        )
        return jsonify(access_token=access_token)
    return jsonify(error='Invalid credentials'), 401