from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

import os

load_dotenv()



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:"+os.getenv("DB_ROOT_PASSWORD")+"@db:3306/"+os.getenv("DB_NAME")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy()
db.init_app(app)

with app.app_context():
    db.create_all()

bcrypt = Bcrypt()
bcrypt.init_app(app)

jwt = JWTManager()
jwt.init_app(app)

migrate = Migrate(app, db)

debug = True if os.getenv('DEBUG') == 'True' else False

from src.models.plan import Plan
from src.models.user import User
from src.models.subscription import Subscription

import src.views.user
import src.views.plan
import src.views.auth
import src.views.subscription
