from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_customers_without_api_key():
    response = client.get("/customers")

    assert response.status_code == 401
    assert response.json()["detail"] == "API Key is missing"