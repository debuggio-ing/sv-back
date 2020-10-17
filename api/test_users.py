from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)


def test_get_single_user():
    response = client.get("/users/4")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 4, 'name': 'Diana', 
        'surname': 'Prince', 
        'age': 28, 'mail': 
        'wonderwoman@justiceleague.com', 'active': True
        }

