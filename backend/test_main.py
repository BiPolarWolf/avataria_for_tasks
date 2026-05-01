from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_main():
    # Делаем запрос к нашему API
    response = client.get("/")
    # Проверяем, что статус код 200 (OK)
    assert response.status_code == 200
    # Проверяем, что в ответе именно то, что мы ожидаем
    assert response.json() == {"hello_world": "hello world"}