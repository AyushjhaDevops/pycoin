from fastapi.testclient import TestClient
from pycoin.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["application"] == "PyCoin"
    assert data["symbol"] == "PYC"


def test_health_endpoint():
    response = client.get("/api/v1/health")

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["status"] == "healthy"
    assert data["data"]["coin"] == "PYC"


def test_openapi_documentation():
    response = client.get("/openapi.json")

    assert response.status_code == 200

    schema = response.json()

    assert schema["info"]["title"] == "PyCoin"
