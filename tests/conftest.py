from src import create_app, db, bcrypt
from src.models.plan import Plan
from src.models.user import User
from src.models.subscription import Subscription
from faker import Faker
from flask_jwt_extended import create_access_token
import pytest
import os

fake = Faker()

@pytest.fixture
def client():        
        
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    
    flask_app = create_app()

    with flask_app.app_context():
        db.create_all()
        yield flask_app.test_client()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def seed_plans():
    plans = [Plan(name=fake.name(), price=fake.random_digit()) for _ in range(15)]
    db.session.add_all(plans)
    db.session.commit()
    return plans

@pytest.fixture
def seed_subscriptions(seed_plans):
    subscriptions = [Subscription(user_id=1, plan_id=plan.id) for plan in seed_plans]
    db.session.add_all(subscriptions)
    db.session.commit()
    return subscriptions


@pytest.fixture
def auth_token():
    User.query.delete()
    db.session.commit()
    user = User(
        name="User Test",
        email="user@test.com",
        password_hash=bcrypt.generate_password_hash("Secret.123").decode('utf-8')
    )
    db.session.add(user)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return token