from flask import request, jsonify
from src import app, db, debug, bcrypt
from src.models.user import User


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(email=data['email'], password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return jsonify(message='User registered'), 201

@app.route('/auth/login', methods=['GET'])
def login():
    return jsonify(message='Login'), 201