## Инструкция для проекта распознавания лиц:

## 📂 Структура проекта

```
faceid_project/
├── config/         # Основной модуль Django
├── faceid/                 # Приложение с API
├── faces_db/               # Каталог с лицами (JPG, PNG)
├── db.sqlite3              # оставил db в гит чтобы было легче тестировать (запускать)
├── .env                    # Настройки, оставил как dot.env чтобы было легче тестировать (запускать)
├── manage.py
└── requirements.txt
```

---

## ⚙️ Установка

### 1. Клонировать репозиторий

```bash
git clone https://github.com/son-of-Altay/faceid-petproject.git
cd faceid-petproject
```

### 2. Создать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Убрать 'dot' из названия `dot.env` файл

### 5. Добавить доп. лица в папку `faces_db/`

Пример:

```
faces_db/
├── oigyrbay.jpg
├── eshenqan.png
└── ...
```

### 6. Запуск проекта

```bash
python manage.py migrate
python manage.py runserver
```

---

## API документация

```
http://127.0.0.1:8000/api/docs/
```

---

## 🔐 Получение токена

### Endpoint:

```
POST /api/token/
```

### Тело запроса:

```json
{
  "username": "admin",
  "password": "admin1"
}
```

Ответ:

```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

> **Примечание:** Добавьте пользователя командой:

```bash
python manage.py createsuperuser
```

---

## 🧠 Распознавание лица

### Endpoint:

```
POST /api/faceid/identify/
```

### Headers:

```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

### Формат запроса:

* Параметр `file` — файл изображения (JPG/PNG)

Пример (curl):

```bash
curl -X POST http://127.0.0.1:8000/api/faceid/identify/ \
  -H "Authorization: Bearer <your_token>" \
  -F "file=@test_face.jpg"
```

### Ответ:

```json
{
  "matched": true,
  "person_id": "oigyrbay"
}
```

---

## 🔄 Автоматическая загрузка базы лиц

Все изображения из `faces_db/` автоматически загружаются при запуске сервера.
