from src import db
from src.models.plan import Plan


def test_list_plans_first_page(client, seed_plans):
    # when
    response = client.get('/plan/')
    
    # then
    assert response.status_code == 200
    
    data = response.get_json()
    assert "data" in data
    assert len(data["data"]) == 10   
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 10    
    assert data["pagination"]["pages"] == 2


def test_list_plans_last_page(client, seed_plans):
    # when
    response = client.get('/plan/?per_page=9&page=2')
    
    # then
    assert response.status_code == 200
    
    data = response.get_json()     
    assert len(data["data"]) == 6
    assert data["pagination"]["page"] == 2
    assert data["pagination"]["per_page"] == 9
    assert data["pagination"]["pages"] == 2

def test_list_plans_name_filter(client, seed_plans):
    
    # given
    plan = Plan(name="Basic", price=10)
    db.session.add(plan)
    db.session.commit()

    # when
    response = client.get('/plan/?name=Basic')
    
    # then
    assert response.status_code == 200
    
    data = response.get_json()    
    assert len(data["data"]) == 1
    assert data["data"][0]["name"] == "Basic"
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 10
    assert data["pagination"]["total"] == 1
    assert data["pagination"]["pages"] == 1

def test_list_empty_plans(client):
    # when
    response = client.get('/plan/')
    
    # then
    assert response.status_code == 200
    data = response.get_json()
    
    assert "data" in data
    assert data["data"] == []  
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 10    
    assert data["pagination"]["pages"] == 0