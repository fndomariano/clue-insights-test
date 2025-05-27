from src.models.plan import Plan
from src import db

def test_delete(client, seed_plans):
    # when
    response = client.delete('/plan/1')
    
    # then
    assert 204 == response.status_code    


def test_not_found(client):
    # when
    response = client.delete('/plan/0')
    
    # then       
    assert 404 == response.status_code
    data = response.get_json()
    assert "error" in data
    assert "The Plan was not found." in data["error"]