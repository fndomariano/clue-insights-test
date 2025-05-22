from src.models.plan import Plan
from src import db

def test_change_status(client, seed_plans):
    # given
    id = 1
    currentStatusPlan = db.session.get(Plan, id).active

    # when
    response = client.post('/plan/'+str(id)+'/changeStatus')
    
    # then
    plan_updated = db.session.get(Plan, id)
    assert 204 == response.status_code
    assert plan_updated.active is not currentStatusPlan
    

def test_not_found(client):
    # when
    response = client.post('/plan/0/changeStatus')
    
    # then       
    assert 404 == response.status_code
    data = response.get_json()
    assert "error" in data
    assert "The Plan was not found." in data["error"]