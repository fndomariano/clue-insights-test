from flask import Response, request, jsonify
from src import app, db, debug
from datetime import datetime


@app.route('/auth/register', methods=['GET'])
def register():
    return jsonify(message='User registered'), 201

@app.route('/auth/login', methods=['GET'])
def login():
    return jsonify(message='Login'), 201