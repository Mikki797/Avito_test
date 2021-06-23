from fastapi.testclient import TestClient

from app.api import app

client = TestClient(app)


def test_create_poll():
    response = client.post('/api/createPoll', json={'name': 'Голосование1', 'choices': ['Вариант1', 'Вариант2']})
    assert response.status_code == 200
    assert isinstance(response.json()['id'], int)
    assert response.json()['name'] == 'Голосование1'
    assert response.json()['choices'] == ['Вариант1', 'Вариант2']


def test_vote():
    response = client.post('/api/createPoll', json={'name': 'Голосование1', 'choices': ['Вариант1', 'Вариант2']})
    id = response.json()['id']
    response = client.post('/api/poll', json={'poll_id': id, 'choice_id': 0})
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_get_result():
    response = client.post('/api/createPoll', json={'name': 'Голосование1', 'choices': ['Вариант1', 'Вариант2']})
    id = response.json()['id']
    client.post('/api/poll', json={'poll_id': id, 'choice_id': 0})
    client.post('/api/poll', json={'poll_id': id, 'choice_id': 0})
    client.post('/api/poll', json={'poll_id': id, 'choice_id': 1})
    response = client.post(f'/api/getResult/{id}')
    assert response.status_code == 200
    assert response.json()['poll_id'] == id
    assert len(response.json()['result']) == 2
    assert response.json()['result'][0]['choice_id'] == 0
    assert response.json()['result'][0]['vote_count'] == 2
    assert response.json()['result'][1]['choice_id'] == 1
    assert response.json()['result'][1]['vote_count'] == 1
