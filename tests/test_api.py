from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_create_poll():
    response = client.post('/api/createPoll', json={'name': 'Голосование1', 'choices': ['Вариант1', 'Вариант2']})
    assert response.status_code == 200
    assert response.json()['name'] == 'Голосование1'
    assert response.json()['choices'] == ['Вариант1', 'Вариант2']