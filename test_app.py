import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_task(client):
    response = client.post('/add', data={
        'task': 'Test Task',
        'jadwal': '2026-04-21T09:00'
    })
    assert response.status_code == 302

def test_format_jadwal():
    jadwal_raw = '2026-04-21T09:00'
    jadwal = jadwal_raw.replace('T', ' ') + ':00'
    assert jadwal == '2026-04-21 09:00:00'