import pytest
from unittest.mock import patch, MagicMock
from app import app
import os
import pymysql

DB_CONFIG = {
    'host': 'db',
    'user': 'root',
    'password': os.environ.get('MYSQL_PASSWORD', 'password'),
    'database': os.environ.get('MYSQL_DATABASE', 'tododb'),
    'cursorclass': pymysql.cursors.DictCursor
}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_homepage_loads(client):
    mock_tasks = [
        {'id': 1, 'title': 'Test Task', 'jadwal': '09:00:00'}
    ]
    with patch('app.get_db') as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        mock_cursor.fetchall.return_value = mock_tasks
        response = client.get('/')
        assert response.status_code == 200

def test_add_task(client):
    with patch('app.get_db') as mock_db:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_db.return_value = mock_conn
        mock_conn.cursor.return_value.__enter__ = MagicMock(return_value=mock_cursor)
        mock_conn.cursor.return_value.__exit__ = MagicMock(return_value=False)
        response = client.post('/add', data={
            'task': 'Test Task',
            'jadwal': '09:00'
        })
        assert response.status_code == 302

def test_format_jadwal():
    jadwal_raw = '2026-04-21T09:00'
    jadwal = jadwal_raw.replace('T', ' ') + ':00'
    assert jadwal == '2026-04-21 09:00:00'