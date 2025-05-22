from src.models.plan import Plan
from src import db

def test_get(client):
    # given
    plan = db.session.get(Plan, 1)

    # when
    response = client.get('/plan/1')
    
    # then
    assert 200 == response.status_code
    
    data = response.get_json()
    assert "name" in data['data'] and plan.name == data['data']['name']
    assert "price" in data['data'] and plan.price == data['data']['price']
    assert "active" in data['data'] and plan.active == data['data']['active']


def test_not_found(client):
    # when
    response = client.get('/plan/0')
    
    # then       
    assert 404 == response.status_code
    data = response.get_json()
    assert "error" in data
    assert "The Plan was not found." in data["error"]