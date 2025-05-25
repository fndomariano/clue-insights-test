from src import app, db, bcrypt
from src.models.plan import Plan
from src.models.user import User
from src.models.subscription import Subscription
import pytest
from faker import Faker
from flask_jwt_extended import create_access_token

fake = Faker()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def seed_plans():
    plans = [Plan(name=fake.name(), price=fake.random_digit()) for _ in range(15)]
    db.session.add_all(plans)
    db.session.commit()
    return plans

@pytest.fixture
def auth_token():
    user = User(
        name="User Test",
        email="user@test.com",
        password_hash=bcrypt.generate_password_hash("Secret.123").decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return token