import pytest
from fastapi.testclient import TestClient
from main import app
from faker import Faker
import jwt
from datetime import datetime, timedelta, timezone
from minio import Minio
from config import MinioConfig
import io

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

@pytest.fixture
def video_data():
    return {
        "name": faker.word()[:3],  # Убедитесь, что длина имени >= 3 символов
        "length_seconds": faker.random_int(min=1, max=3600),
        "size": faker.random_int(min=1, max=1000)
    }

@pytest.fixture
def minio_client():
    config = MinioConfig()
    client = Minio(
        f"{config.host}:{config.port}",
        access_key=config.login,
        secret_key=config.password,
        secure=False
    )
    return client

def upload_video_to_minio(minio_client, bucket_name, file_name, content):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
    minio_client.put_object(bucket_name, file_name, io.BytesIO(content), length=len(content))

def log_response(action: str, response, data=None):
    print(f"\n{'='*20} {action} {'='*20}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    if data:
        print(f"Input Data: {data}")
    print(f"{'='*60}\n")

def test_full_flow(user_data, updated_user_data, video_data, minio_client):
    # 1. Создание пользователя
    create_user_response = client.post("/users", json=user_data)
    log_response("Создание пользователя", create_user_response, user_data)
    assert create_user_response.status_code == 201
    assert "token" in create_user_response.json()
    token = create_user_response.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # --- Тесты на создание пользователя ---
    # Повторное создание пользователя
    create_user_conflict_response = client.post("/users", json=user_data)
    log_response("Повторное создание пользователя", create_user_conflict_response, user_data)
    assert create_user_conflict_response.status_code == 409
    assert create_user_conflict_response.json()["message"] == "Conflict field/fields"

    # Создание пользователя с некорректными данными
    invalid_user_data = user_data.copy()
    invalid_user_data["email"] = "invalid_email"
    create_user_invalid_response = client.post("/users", json=invalid_user_data)
    log_response("Создание пользователя с некорректными данными", create_user_invalid_response, invalid_user_data)
    assert create_user_invalid_response.status_code == 422
    assert "problem_fields" in create_user_invalid_response.json()

    # --- Тесты на редактирование пользователя ---
    # Успешное редактирование
    update_user_response = client.put("/users/me", json={**updated_user_data, 'current_password': user_data['password']}, headers=headers)
    log_response("Редактирование пользователя", update_user_response, {**updated_user_data, 'current_password': user_data['password']})
    assert update_user_response.status_code == 200

    # Редактирование с некорректными данными
    invalid_update_data = updated_user_data.copy()
    invalid_update_data["email"] = "invalid_email"
    update_user_invalid_response = client.put("/users/me", json={**invalid_update_data, 'current_password': user_data['password']}, headers=headers)
    log_response("Редактирование с некорректными данными", update_user_invalid_response, {**invalid_update_data, 'current_password': user_data['password']})
    assert update_user_invalid_response.status_code == 422

    # Редактирование без текущего пароля
    update_user_no_password_response = client.put("/users/me", json=updated_user_data, headers=headers)
    log_response("Редактирование без текущего пароля", update_user_no_password_response, updated_user_data)
    assert update_user_no_password_response.status_code == 400
    assert update_user_no_password_response.json()["message"] == "requires an up-to-date password to update password or email"

    # Редактирование несуществующего пользователя
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    update_nonexistent_user_response = client.put("/users/me", json=updated_user_data, headers=invalid_headers)
    log_response("Редактирование несуществующего пользователя", update_nonexistent_user_response, updated_user_data)
    assert update_nonexistent_user_response.status_code == 401

    # --- Тесты на получение данных пользователя ---
    # Успешное получение данных
    get_user_response = client.get("/users/me", headers=headers)
    log_response("Получение данных пользователя", get_user_response)
    assert get_user_response.status_code == 200
    assert get_user_response.json()["login"] == updated_user_data["login"]

    # Получение данных с некорректным токеном
    get_user_invalid_token_response = client.get("/users/me", headers=invalid_headers)
    log_response("Получение данных с некорректным токеном", get_user_invalid_token_response)
    assert get_user_invalid_token_response.status_code == 401

    # Получение данных с истекшим токеном
    now = datetime.now(timezone.utc)
    payload = {
        "sub": 'user_id',
        "exp": now - timedelta(days=1),
        "nbf": now,
        "iat": now,
    }
    expired_token = jwt.encode(payload, 'default', algorithm="HS256")
    expired_headers = {"Authorization": f"Bearer {expired_token}"}
    expired_token_response = client.get("/users/me", headers=expired_headers)
    log_response("Получение данных с истекшим токеном", expired_token_response)
    assert expired_token_response.status_code == 401
    assert expired_token_response.json()["message"] == "Token has expired"

    # --- Тесты на создание видео ---
    # Успешное создание видео
    create_video_response = client.post("/users/me/videos", json=video_data, headers=headers)
    log_response("Создание видео", create_video_response, video_data)
    assert create_video_response.status_code == 201
    assert "upload_link" in create_video_response.json()

    # Загрузка видео в MinIO
    video_content = b"dummy video content"
    upload_video_to_minio(minio_client, "video", video_data["name"], video_content)
    assert minio_client.stat_object("video", video_data["name"])

    # Создание видео с некорректными данными
    invalid_video_data = video_data.copy()
    invalid_video_data["length_seconds"] = 5000
    create_video_invalid_response = client.post("/users/me/videos", json=invalid_video_data, headers=headers)
    log_response("Создание видео с некорректными данными", create_video_invalid_response, invalid_video_data)
    assert create_video_invalid_response.status_code == 422
    assert "problem_fields" in create_video_invalid_response.json()

    # Создание видео с дублирующимся именем
    create_video_duplicate_response = client.post("/users/me/videos", json=video_data, headers=headers)
    log_response("Создание видео с дублирующимся именем", create_video_duplicate_response, video_data)
    assert create_video_duplicate_response.status_code == 409
    assert create_video_duplicate_response.json()["message"] == "Conflict field/fields"

    # Создание видео без авторизации
    create_video_unauthorized_response = client.post("/users/me/videos", json=video_data)
    log_response("Создание видео без авторизации", create_video_unauthorized_response, video_data)
    assert create_video_unauthorized_response.status_code == 401

    # --- Тесты на генерацию токена ---
    # Успешная генерация токена
    generate_token_response = client.post("/users/me/token", json={"login": updated_user_data["login"], "password": updated_user_data["password"]})
    log_response("Генерация токена", generate_token_response, {"login": updated_user_data["login"], "password": updated_user_data["password"]})
    assert generate_token_response.status_code == 201
    assert "token" in generate_token_response.json()

    # Генерация токена с некорректными данными
    invalid_token_data = {"login": updated_user_data["login"], "password": "wrong_password"}
    generate_token_invalid_response = client.post("/users/me/token", json=invalid_token_data)
    log_response("Генерация токена с некорректными данными", generate_token_invalid_response, invalid_token_data)
    assert generate_token_invalid_response.status_code == 404
    assert generate_token_invalid_response.json()["message"] == "User not found"

    # --- Тесты на тепловую карту ---
    # Успешное создание тепловой карты
    heatmap_data = {"video_name": video_data["name"]}
    create_heatmap_response = client.post("/users/me/videos/heatmap", json=heatmap_data, headers=headers)
    log_response("Создание тепловой карты", create_heatmap_response, heatmap_data)
    assert create_heatmap_response.status_code == 201
    assert "upload_link" in create_heatmap_response.json()

    # Создание тепловой карты для несуществующего видео
    invalid_heatmap_data = {"video_name": "non_existent_video"}
    create_heatmap_invalid_response = client.post("/users/me/videos/heatmap", json=invalid_heatmap_data, headers=headers)
    log_response("Создание тепловой карты для несуществующего видео", create_heatmap_invalid_response, invalid_heatmap_data)
    assert create_heatmap_invalid_response.status_code == 404
    assert create_heatmap_invalid_response.json()["message"] == "Video not found"

    # Повторное создание тепловой карты
    create_heatmap_conflict_response = client.post("/users/me/videos/heatmap", json=heatmap_data, headers=headers)
    log_response("Повторное создание тепловой карты", create_heatmap_conflict_response, heatmap_data)
    assert create_heatmap_conflict_response.status_code == 409
    assert create_heatmap_conflict_response.json()["message"] == "Conflict field/fields"

    # --- Тесты на поиск видео ---
    # Успешный поиск видео
    search_params = {"count": 1, "date": "2025-03-02"}
    search_video_response = client.get("/users/me/videos/search", params=search_params, headers=headers)
    log_response("Поиск видео", search_video_response, search_params)
    assert search_video_response.status_code == 200
    assert "videos" in search_video_response.json()

    # Поиск видео с некорректными параметрами
    invalid_search_params = {"count": -1, "date": "invalid_date"}
    search_video_invalid_response = client.get("/users/me/videos/search", params=invalid_search_params, headers=headers)
    log_response("Поиск видео с некорректными параметрами", search_video_invalid_response, invalid_search_params)
    assert search_video_invalid_response.status_code == 422

    # --- Тесты на получение ссылки на скачивание видео ---
    # Получение ссылки на несуществующее видео
    invalid_video_name = "non_existent_video"
    get_unload_link_not_found_response = client.get(f"/users/me/videos/unload_link?name={invalid_video_name}", headers=headers)
    log_response("Получение ссылки на несуществующее видео", get_unload_link_not_found_response)
    assert get_unload_link_not_found_response.status_code == 404
    assert get_unload_link_not_found_response.json()["message"] == "Video not found"
    
    # --- Тесты на удаление пользователя ---
    # Успешное удаление пользователя
    delete_user_response = client.delete("/users/me", headers=headers)
    log_response("Удаление пользователя", delete_user_response)
    assert delete_user_response.status_code == 200

    # Повторное удаление пользователя
    delete_user_again_response = client.delete("/users/me", headers=headers)
    log_response("Повторное удаление пользователя", delete_user_again_response)
    assert delete_user_again_response.status_code == 404
    assert delete_user_again_response.json()["message"] == "User not found"

    # Удаление пользователя без авторизации
    delete_user_unauthorized_response = client.delete("/users/me")
    log_response("Удаление пользователя без авторизации", delete_user_unauthorized_response)
    assert delete_user_unauthorized_response.status_code == 401

    # Проверка, что пользователь удален
    get_user_after_delete_response = client.get("/users/me", headers=headers)
    log_response("Проверка удаления пользователя", get_user_after_delete_response)
    assert get_user_after_delete_response.status_code == 404








