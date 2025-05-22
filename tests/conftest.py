from src import app, db
from src.models.plan import Plan
import pytest
from faker import Faker

fake = Faker()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        seed_database()
        yield app.test_client()
        db.session.remove()
        db.drop_all()

def seed_database():
    create_plans()

def create_plans():
    plans = [Plan(name=fake.name(), price=fake.random_digit()) for _ in range(15)]
    db.session.bulk_save_objects(plans)
    db.session.commit()