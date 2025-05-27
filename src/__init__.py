from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os, logging

load_dotenv()

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)
    
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    register_routes(app)
    
    with app.app_context():
        db.create_all()
    
    return app


def register_routes(app):
    from src.views import user, plan, auth, subscription
    app.register_blueprint(user.bp)
    app.register_blueprint(plan.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(subscription.bp)


# logging.basicConfig()
# logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


debug = True if os.getenv('DEBUG') == 'True' else False

from src.models.plan import Plan
from src.models.user import User
from src.models.subscription import Subscription

