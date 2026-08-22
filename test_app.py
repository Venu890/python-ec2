import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"EC2 Deployment Dashboard" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["status"] == "healthy"
    assert "version" in json_data
    assert "timestamp" in json_data

def test_api_info_endpoint(client):
    response = client.get("/api/info")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["app_name"] == "EC2 Deployment Verification App"
    assert "hostname" in json_data

def test_counter_api(client):
    # Test initial counter
    res = client.get("/api/counter")
    assert res.status_code == 200
    init_count = res.get_json()["count"]

    # Increment counter
    inc_res = client.post("/api/counter", json={"action": "increment"})
    assert inc_res.status_code == 200
    assert inc_res.get_json()["count"] == init_count + 1
