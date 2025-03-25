import pytest
from fastapi.testclient import TestClient
from main import app
from faker import Faker

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

def log_response(action: str, response, data=None):
    print(f"\n{'='*20} {action} {'='*20}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Content: {response.content.decode('utf-8')}")
    if data:
        print(f"Input Data: {data}")
    print(f"{'='*60}\n")

def test_full_flow(user_data, updated_user_data, video_data):
    # 1. Создание пользователя
    create_user_response = client.post("/users", json=user_data)
    log_response("Создание пользователя", create_user_response, user_data)
    assert create_user_response.status_code == 201
    assert "token" in create_user_response.json()
    token = create_user_response.json()["token"]

    headers = {"Authorization": f"Bearer {token}"}

    # Проверка ошибки при повторном создании пользователя
    create_user_conflict_response = client.post("/users", json=user_data)
    log_response("Повторное создание пользователя", create_user_conflict_response, user_data)
    assert create_user_conflict_response.status_code == 409

    # Проверка ошибки при создании пользователя с некорректными данными
    invalid_user_data = user_data.copy()
    invalid_user_data["email"] = "invalid_email"
    create_user_invalid_response = client.post("/users", json=invalid_user_data)
    log_response("Создание пользователя с некорректными данными", create_user_invalid_response, invalid_user_data)
    assert create_user_invalid_response.status_code == 422

    # 2. Редактирование пользователя
    update_user_response = client.put("/users", json={**updated_user_data, 'current_password': user_data['password']}, headers=headers)
    log_response("Редактирование пользователя", update_user_response, {**updated_user_data, 'current_password': user_data['password']})
    assert update_user_response.status_code == 200

    # Проверка ошибки при редактировании с некорректными данными
    invalid_update_data = updated_user_data.copy()
    invalid_update_data["email"] = "invalid_email"
    update_user_invalid_response = client.put("/users", json={**invalid_update_data, 'current_password': user_data['password']}, headers=headers)
    log_response("Редактирование с некорректными данными", update_user_invalid_response, {**invalid_update_data, 'current_password': user_data['password']})
    assert update_user_invalid_response.status_code == 422

    # Проверка ошибки при редактировании без текущего пароля
    update_user_no_password_response = client.put("/users", json=updated_user_data, headers=headers)
    log_response("Редактирование без текущего пароля", update_user_no_password_response, updated_user_data)
    assert update_user_no_password_response.status_code == 400

    # 3. Получение данных пользователя
    get_user_response = client.get("/users", headers=headers)
    log_response("Получение данных пользователя", get_user_response)
    assert get_user_response.status_code == 200
    assert get_user_response.json()["login"] == updated_user_data["login"]

    # Проверка ошибки при получении данных с некорректным токеном
    invalid_headers = {"Authorization": "Bearer invalid_token"}
    get_user_invalid_token_response = client.get("/users", headers=invalid_headers)
    log_response("Получение данных с некорректным токеном", get_user_invalid_token_response)
    assert get_user_invalid_token_response.status_code == 401

    # 4. Создание видео
    create_video_response = client.post("/user/videos", json=video_data, headers=headers)
    log_response("Создание видео", create_video_response, video_data)
    assert create_video_response.status_code == 201
    assert "upload_link" in create_video_response.json()

    # Проверка ошибки при создании видео с некорректными данными
    invalid_video_data = video_data.copy()
    invalid_video_data["length_seconds"] = 5000  # Некорректное значение
    create_video_invalid_response = client.post("/user/videos", json=invalid_video_data, headers=headers)
    log_response("Создание видео с некорректными данными", create_video_invalid_response, invalid_video_data)
    assert create_video_invalid_response.status_code == 422

    # Проверка ошибки при создании видео с дублирующимся именем
    create_video_duplicate_response = client.post("/user/videos", json=video_data, headers=headers)
    log_response("Создание видео с дублирующимся именем", create_video_duplicate_response, video_data)
    assert create_video_duplicate_response.status_code == 409

    # 5. Создание тепловой карты
    heatmap_data = {"video_name": video_data["name"]}
    create_heatmap_response = client.post("/user/videos/heatmap", json=heatmap_data, headers=headers)
    log_response("Создание тепловой карты", create_heatmap_response, heatmap_data)
    assert create_heatmap_response.status_code == 201
    assert "upload_link" in create_heatmap_response.json()

    # Проверка ошибки при повторном создании тепловой карты
    create_heatmap_conflict_response = client.post("/user/videos/heatmap", json=heatmap_data, headers=headers)
    log_response("Повторное создание тепловой карты", create_heatmap_conflict_response, heatmap_data)
    assert create_heatmap_conflict_response.status_code == 409

    # Проверка ошибки при создании тепловой карты для несуществующего видео
    invalid_heatmap_data = {"video_name": "non_existent_video"}
    create_heatmap_invalid_response = client.post("/user/videos/heatmap", json=invalid_heatmap_data, headers=headers)
    log_response("Создание тепловой карты для несуществующего видео", create_heatmap_invalid_response, invalid_heatmap_data)
    assert create_heatmap_invalid_response.status_code == 404

    # 6. Поиск видео
    search_params = {
        "count": 1,
        "date": "2025-03-02"
    }
    search_video_response = client.get("/user/videos/search", params=search_params, headers=headers)
    log_response("Поиск видео", search_video_response, search_params)
    assert search_video_response.status_code == 200
    assert "videos" in search_video_response.json()

    # Проверка ошибки при поиске видео с некорректными параметрами
    invalid_search_params = {
        "count": -1,  # Некорректное значение
        "date": "invalid_date"
    }
    search_video_invalid_response = client.get("/user/videos/search", params=invalid_search_params, headers=headers)
    log_response("Поиск видео с некорректными параметрами", search_video_invalid_response, invalid_search_params)
    assert search_video_invalid_response.status_code == 422

    # 7. Удаление пользователя
    delete_user_response = client.delete("/users", headers=headers)
    log_response("Удаление пользователя", delete_user_response)
    assert delete_user_response.status_code == 200

    # Проверка ошибки при повторном удалении пользователя
    delete_user_again_response = client.delete("/users", headers=headers)
    log_response("Повторное удаление пользователя", delete_user_again_response)
    assert delete_user_again_response.status_code == 404

    # 8. Проверка, что пользователь удален
    get_user_after_delete_response = client.get("/users", headers=headers)
    log_response("Проверка удаления пользователя", get_user_after_delete_response)
    assert get_user_after_delete_response.status_code == 404
