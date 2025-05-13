from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://"+os.getenv('DB_USER')+":"+os.getenv('DB_PASSWORD')+"@db:3306"+"/"+os.getenv('DB_DATABASE')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')

db = SQLAlchemy()
db.init_app(app)

debug = True if os.getenv('DEBUG') == 'True' else False

from src.views import auth