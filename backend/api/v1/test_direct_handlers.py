import requests
from faker import Faker
import jwt
from datetime import datetime, timedelta, timezone
from minio import Minio
from config import MinioConfig
import io

faker = Faker()

BASE_URL = "http://217.114.10.197:8000"  # адрес вашего сервера

def log_response(action: str, response, data=None):
    print(f"\n{'='*20} {action} {'='*20}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.text}")
    if data:
        print(f"Input Data: {data}")
    print(f"{'='*60}\n")

# Функции для создания данных
def user_data():
    return {
        "login": faker.user_name(),
        "email": faker.email(),
        "password": faker.password()
    }

def updated_user_data():
    return {
        "login": faker.user_name(),
        "email": faker.email(),
        "password": faker.password()
    }

def video_data():
    return {
        "name": faker.word()[:3],  # Убедитесь, что длина имени >= 3 символов
        "length_seconds": faker.random_int(min=1, max=3600),
        "size": faker.random_int(min=1, max=1000)
    }

def minio_client():
    # Используем тот же сервер, что и указанный в BASE_URL
    config = MinioConfig(
        host="217.114.10.197",  # IP-адрес сервера
        port=9000,  # Порт MinIO
        login="minio",  # Логин MinIO
        password="password"  # Пароль MinIO
    )
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

def test_full_flow():
    # 1. Создание пользователя
    user = user_data()
    create_user_response = requests.post(f"{BASE_URL}/users", json=user)
    log_response("Создание пользователя", create_user_response, user)
    assert create_user_response.status_code == 201
    assert "token" in create_user_response.json()
    token = create_user_response.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # --- Тесты на создание пользователя ---
    # Повторное создание пользователя
    create_user_conflict_response = requests.post(f"{BASE_URL}/users", json=user)
    log_response("Повторное создание пользователя", create_user_conflict_response, user)
    assert create_user_conflict_response.status_code == 409
    assert create_user_conflict_response.json()["message"] == "Conflict field/fields"

    # --- Тесты на редактирование пользователя ---
    updated_user = updated_user_data()
    update_user_response = requests.put(f"{BASE_URL}/users/me", json={**updated_user, 'current_password': user['password']}, headers=headers)
    log_response("Редактирование пользователя", update_user_response, {**updated_user, 'current_password': user['password']})
    assert update_user_response.status_code == 200

    # --- Тесты на получение данных пользователя ---
    get_user_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    log_response("Получение данных пользователя", get_user_response)
    assert get_user_response.status_code == 200
    assert get_user_response.json()["login"] == updated_user["login"]

    # --- Тесты на создание видео ---
    video = video_data()
    create_video_response = requests.post(f"{BASE_URL}/users/me/videos", json=video, headers=headers)
    log_response("Создание видео", create_video_response, video)
    assert create_video_response.status_code == 201
    assert "upload_link" in create_video_response.json()

    # Загрузка видео в MinIO
    video_content = b"dummy video content"
    client = minio_client()
    upload_video_to_minio(client, "video", video["name"], video_content)
    assert client.stat_object("video", video["name"])

    # --- Тесты на создание видео с некорректными данными ---
    invalid_video_data = video.copy()
    invalid_video_data["length_seconds"] = 5000
    create_video_invalid_response = requests.post(f"{BASE_URL}/users/me/videos", json=invalid_video_data, headers=headers)
    log_response("Создание видео с некорректными данными", create_video_invalid_response, invalid_video_data)
    assert create_video_invalid_response.status_code == 422
    assert "problem_fields" in create_video_invalid_response.json()

    # --- Тесты на создание видео с дублирующимся именем ---
    create_video_duplicate_response = requests.post(f"{BASE_URL}/users/me/videos", json=video, headers=headers)
    log_response("Создание видео с дублирующимся именем", create_video_duplicate_response, video)
    assert create_video_duplicate_response.status_code == 409
    assert create_video_duplicate_response.json()["message"] == "Conflict field/fields"

    # --- Тесты на создание видео без авторизации ---
    create_video_unauthorized_response = requests.post(f"{BASE_URL}/users/me/videos", json=video)
    log_response("Создание видео без авторизации", create_video_unauthorized_response, video)
    assert create_video_unauthorized_response.status_code == 401

    # --- Тесты на поиск видео ---
    search_params = {"count": 1, "date": "2025-03-02"}
    search_video_response = requests.get(f"{BASE_URL}/users/me/videos/search", params=search_params, headers=headers)
    log_response("Поиск видео", search_video_response, search_params)
    assert search_video_response.status_code == 200
    assert "videos" in search_video_response.json()

    invalid_search_params = {"count": -1, "date": "invalid_date"}
    search_video_invalid_response = requests.get(f"{BASE_URL}/users/me/videos/search", params=invalid_search_params, headers=headers)
    log_response("Поиск видео с некорректными параметрами", search_video_invalid_response, invalid_search_params)
    assert search_video_invalid_response.status_code == 422

    # --- Тесты на получение ссылки на скачивание видео ---
    invalid_video_name = "non_existent_video"
    get_unload_link_not_found_response = requests.get(f"{BASE_URL}/users/me/videos/unload_link?name={invalid_video_name}", headers=headers)
    log_response("Получение ссылки на несуществующее видео", get_unload_link_not_found_response)
    assert get_unload_link_not_found_response.status_code == 404
    assert get_unload_link_not_found_response.json()["message"] == "Video not found"

    # --- Тесты на тепловую карту ---
    heatmap_data = {"video_name": video["name"]}
    create_heatmap_response = requests.post(f"{BASE_URL}/users/me/videos/heatmap", json=heatmap_data, headers=headers)
    log_response("Создание тепловой карты", create_heatmap_response, heatmap_data)
    assert create_heatmap_response.status_code == 201
    assert "upload_link" in create_heatmap_response.json()

    # --- Тесты на тепловую карту с некорректными данными ---
    invalid_heatmap_data = {"video_name": "non_existent_video"}
    create_heatmap_invalid_response = requests.post(f"{BASE_URL}/users/me/videos/heatmap", json=invalid_heatmap_data, headers=headers)
    log_response("Создание тепловой карты для несуществующего видео", create_heatmap_invalid_response, invalid_heatmap_data)
    assert create_heatmap_invalid_response.status_code == 404
    assert create_heatmap_invalid_response.json()["message"] == "Video not found"

    create_heatmap_conflict_response = requests.post(f"{BASE_URL}/users/me/videos/heatmap", json=heatmap_data, headers=headers)
    log_response("Повторное создание тепловой карты", create_heatmap_conflict_response, heatmap_data)
    assert create_heatmap_conflict_response.status_code == 409
    assert create_heatmap_conflict_response.json()["message"] == "Conflict field/fields"

    # --- Тесты на удаление пользователя ---
    delete_user_response = requests.delete(f"{BASE_URL}/users/me", headers=headers)
    log_response("Удаление пользователя", delete_user_response)
    assert delete_user_response.status_code == 200

    delete_user_again_response = requests.delete(f"{BASE_URL}/users/me", headers=headers)
    log_response("Повторное удаление пользователя", delete_user_again_response)
    assert delete_user_again_response.status_code == 404
    assert delete_user_again_response.json()["message"] == "User not found"

    delete_user_unauthorized_response = requests.delete(f"{BASE_URL}/users/me")
    log_response("Удаление пользователя без авторизации", delete_user_unauthorized_response)
    assert delete_user_unauthorized_response.status_code == 401

    # Проверка, что пользователь удален
    get_user_after_delete_response = requests.get(f"{BASE_URL}/users/me", headers=headers)
    log_response("Проверка удаления пользователя", get_user_after_delete_response)
    assert get_user_after_delete_response.status_code == 404
