import pytest
from fastapi.testclient import TestClient
from main import app
from faker import Faker
import json
import asyncio
client = TestClient(app)

faker = Faker()


    
@pytest.fixture
def user_data():
    return {
        "login": faker.user_name(),
        "email": faker.email(),
        "password": faker.password()
    }

@pytest.fixture
def updated_user_data():
    return {
        "login": faker.user_name(),
        "email": faker.email(),
        "password": faker.password()
    }
    


def test_user_crud(user_data, updated_user_data):

    create_response = client.post("/users", json=user_data)
    
    assert create_response.status_code == 201
    assert "token" in create_response.json()
    token = create_response.json()["token"]

    # Try to create the same user again to check for conflict
    create_response_conflict = client.post("/users", json=user_data)
    assert create_response_conflict.status_code == 409

    headers = {"Authorization": f"Bearer {token}"}

    update_response = client.put("/users", json={**updated_user_data, 'current_password': user_data['password']}, headers=headers)
    assert update_response.status_code == 200

    # Try to update the user with invalid data
    invalid_update_data = updated_user_data.copy()
    invalid_update_data["email"] = "invalid_email"
    update_response_invalid = client.put("/users", json={**invalid_update_data, 'current_password': user_data['password']}, headers=headers)
    assert update_response_invalid.status_code == 422

    get_response = client.get("/users", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["login"] == updated_user_data["login"]

    # Try to get the user with invalid token
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    get_response_invalid_token = client.get("/users", headers=invalid_headers)
    assert get_response_invalid_token.status_code == 401

    delete_response = client.delete("/users", headers=headers)
    assert delete_response.status_code == 200

    get_response_after_delete = client.get("/users", headers=headers)
    assert get_response_after_delete.status_code == 404

    # Try to delete the user again
    delete_response_after_delete = client.delete("/users", headers=headers)
    assert delete_response_after_delete.status_code == 404


def test_search_user_video_no_videos(user_data):
    # Создаем пользователя
    create_response = client.post("/users", json=user_data)
    assert create_response.status_code == 201
    token = create_response.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Проверяем поиск видео, когда видео отсутствуют
    search_params = {
        "count": 1,
        "date": "2025-03-02"
    }
    search_response = client.get("/videos/search", params=search_params, headers=headers)
    assert search_response.status_code == 200
    assert "videos" in search_response.json()
    assert len(search_response.json()["videos"]) != 0
    assert search_response.json()["cursor"] is None
