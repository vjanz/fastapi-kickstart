from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_create_item(test_client: TestClient) -> None:
    response = test_client.post("/api/v1/items/", json={"name": "Test Item"})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"


def test_read_item(test_client: TestClient) -> None:
    create_response = test_client.post("/api/v1/items/", json={"name": "Test Item"})
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]

    read_response = test_client.get(f"/api/v1/items/{item_id}")
    assert read_response.status_code == 200
    assert read_response.json()["name"] == "Test Item"


def test_read_items(test_client: TestClient) -> None:
    response = test_client.get("/api/v1/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_non_existent_item(test_client: TestClient) -> None:
    response = test_client.post("/api/v1/items/", json={"name": "Test Item"})
    assert response.status_code == 201
    response = test_client.get("/api/v1/items/999999999")
    assert response.status_code == 404
