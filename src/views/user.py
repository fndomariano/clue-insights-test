from flask import request, jsonify
from marshmallow import ValidationError
from src import app, db, bcrypt
from src.models.user import User
from src.schemas.user import UserSchema


@app.route('/user/register', methods=['POST'])
def register():
    schema = UserSchema()
    
    try:
        data = schema.load(request.get_json())                
    except ValidationError as err:
        return jsonify(errors=err.messages), 422
    
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        
    user = User(name=data['name'], email=data['email'], password_hash=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify(message='User registered'), 201
        