from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_revenue():
    response = client.get("/analytics/revenue")

    assert response.status_code == 200

    data = response.json()

    assert "total_revenue" in data
    assert "completed_orders" in data
    assert data["total_revenue"] >= 0
    assert data["completed_orders"] >= 0