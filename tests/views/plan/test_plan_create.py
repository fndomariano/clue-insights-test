from src import app, db
from src.models.plan import Plan
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()
    
def test_add(client):
    # given
    payload = {
        'name': 'Premium',
        'price': 49.99
    }
    
    # when
    response = client.post('/plan', json=payload)
    
    # then
    plan = Plan.query.filter_by(name=payload['name']).first()
    assert 201 == response.status_code
    assert plan is not None
    assert plan.price == payload['price']
    

def test_required_validation(client):
        
    # when
    response = client.post('/plan', json={})
    
    # then        
    assert 422 == response.status_code