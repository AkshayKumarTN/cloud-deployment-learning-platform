"""Test suite for DeployHub application"""
import pytest
import json
from src.app import app, calculate_sum

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_calculate_sum():
    """Test calculation function"""
    assert calculate_sum(2, 3) == 5
    assert calculate_sum(-1, 1) == 0
    assert calculate_sum(0, 0) == 0
    assert calculate_sum(100, 200) == 300

def test_home_page(client):
    """Test home page loads"""
    response = client.get('/')
    assert response.status_code == 200
    assert b'DeployHub' in response.data

def test_aws_page(client):
    """Test AWS page loads"""
    response = client.get('/aws')
    assert response.status_code == 200
    assert b'AWS' in response.data

def test_digitalocean_page(client):
    """Test Digital Ocean page loads"""
    response = client.get('/digitalocean')
    assert response.status_code == 200
    assert b'Digital Ocean' in response.data

def test_demo_page(client):
    """Test demo page loads"""
    response = client.get('/demo')
    assert response.status_code == 200

def test_health(client):
    """Test health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_metrics(client):
    """Test metrics endpoint"""
    response = client.get('/metrics')
    assert response.status_code == 200

def test_api_calculate(client):
    """Test API calculation"""
    response = client.post('/api/calculate',
                          data=json.dumps({'a': 5, 'b': 7}),
                          content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 12

def test_api_invalid(client):
    """Test API with invalid input"""
    response = client.post('/api/calculate',
                          data=json.dumps({'a': 'invalid'}),
                          content_type='application/json')
    assert response.status_code == 400
