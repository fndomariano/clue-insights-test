from src import db
from src.models.subscription import Subscription


def test_list_history_first_page(client, seed_subscriptions, auth_token):    
    # when
    response = client.get(
        '/subscriptions/history',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # then
    assert response.status_code == 200
    
    data = response.get_json()
    assert "data" in data
    assert len(data["data"]) == 10    


def test_list_history_last_page(client, seed_subscriptions, auth_token):
    # when
    response = client.get(
        '/subscriptions/history?per_page=9&page=2',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # then
    assert response.status_code == 200
    
    data = response.get_json()     
    assert len(data["data"]) == 6


def test_list_empty_history(client, auth_token):
    # when
    response = client.get(
        '/subscriptions/history',
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    
    # then
    assert response.status_code == 200
    data = response.get_json()
    
    assert "data" in data
    assert data["data"] == []