#!/bin/bash

API_URL="http://217.114.10.197:8000"
UUID=$(uuidgen)
LOGIN="testuser_$UUID"
EMAIL="test_$UUID@example.com"
PASSWORD="TestPass123!"

# Функция для форматирования JSON
function pretty() {
  echo "$1" | jq '.' 2>/dev/null || echo "$1"
}

# Функция для выполнения HTTP-запросов
function curl_request() {
  local method="$1"
  local endpoint="$2"
  local data="$3"
  local auth="$4"
  local title="$5"

  echo -e "\n=== $title ==="
  echo "Request: $data"

  # Выполнение запроса
  response=$(curl -s -w "\n[STATUS_CODE]%{http_code}" -X "$method" "$API_URL$endpoint" \
    -H "Content-Type: application/json" \
    ${auth:+-H "Authorization: Bearer $auth"} \
    -d "$data")

  # Извлечение статус-кода и тела ответа
  status_code=$(echo "$response" | grep '\[STATUS_CODE\]' | sed 's/\[STATUS_CODE\]//')
  body=$(echo "$response" | sed '/\[STATUS_CODE\]/d')

  echo "Response (status $status_code):"
  pretty "$body"
}

# Создание пользователя
user_data=$(jq -n --arg login "$LOGIN" --arg email "$EMAIL" --arg password "$PASSWORD" \
  '{login: $login, email: $email, password: $password}')
curl_request POST "/users" "$user_data" "" "Создание пользователя"

# Повторное создание пользователя
curl_request POST "/users" "$user_data" "" "Повторное создание пользователя"

# Создание пользователя с некорректными данными
invalid_user_data=$(jq -n --arg login "baduser" --arg email "not-an-email" --arg password "123" \
  '{login: $login, email: $email, password: $password}')
curl_request POST "/users" "$invalid_user_data" "" "Создание пользователя с некорректными данными"

# Обновление пользователя
updated_email="new_test_$UUID@example.com"
updated_password="NewPass123!"
updated_user_data=$(jq -n --arg login "$LOGIN" --arg email "$updated_email" --arg password "$updated_password" \
  '{login: $login, email: $email, password: $password}')
curl_request PUT "/users/" "$updated_user_data" "" "Обновление пользователя"

# Генерация нового токена
token_data=$(jq -n --arg login "$LOGIN" --arg password "$updated_password" \
  '{login: $login, password: $password}')
token=$(curl -s -X POST "$API_URL/token" -H "Content-Type: application/json" -d "$token_data" | jq -r '.access_token')
echo -e "\nToken: $token"

# Получение данных пользователя
curl_request GET "/users/me" "" "$token" "Получение данных пользователя"

# Создание видео
video_data=$(jq -n --arg filename "test.mp4" --arg title "Test video" \
  '{filename: $filename, metadata: {title: $title}}')
curl_request POST "/videos" "$video_data" "$token" "Создание видео"

# Создание тепловой карты
heatmap_data=$(jq -n --arg video_id "dummy_id" '{video_id: $video_id}')
curl_request POST "/heatmaps" "$heatmap_data" "$token" "Создание тепловой карты"

# Поиск видео
search_data=$(jq -n --arg query "test" '{query: $query}')
curl_request POST "/videos/search" "$search_data" "$token" "Поиск видео"

# Получение ссылки на скачивание видео
curl_request GET "/videos/dummy_id/download-link" "" "$token" "Получение ссылки на скачивание видео"

# Удаление пользователя
curl_request DELETE "/users/me" "" "$token" "Удаление пользователя"
