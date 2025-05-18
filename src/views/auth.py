from flask import jsonify
from src import app

@app.route('/auth/login', methods=['GET'])
def login():
    return jsonify(message='Login'), 201