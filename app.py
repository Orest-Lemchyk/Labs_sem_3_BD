# app.py (у корені твоєї папки lab4)
import os
from flask import Flask, g, jsonify
from config.db import Base, engine, SessionLocal
from dotenv import load_dotenv

# Завантажуємо .env файл
load_dotenv() 

# --- FIX: Попереднє завантаження ВСІХ моделей ---
# Це критично важливо, щоб уникнути помилок "Circular Import".
# Ми імпортуємо всі файли з 'domain/' тут, на самому початку.
try:
    from domain import associations, artist, album, label, playlist, song, user, user_currently_playing
except ImportError as e:
    print(f"Помилка імпорту моделей. Переконайся, що папка 'domain' існує. Помилка: {e}")
# --- Кінець FIX ---


# --- 1. Імпортуємо всі твої Blueprints (Контролери) ---
from routes.artist_routes import artist_bp
from routes.user_routes import user_bp
from routes.song_routes import song_bp
from routes.album_routes import album_bp
from routes.playlist_routes import playlist_bp
from routes.label_routes import label_bp

# --- 2. Створюємо Flask додаток ---
app = Flask(__name__)

# --- 3. Керування сесіями бази даних ---
# Це "магія", яка робить g.session доступним у всіх твоїх
# файлах /routes і гарантує, що сесія
# коректно відкривається і закривається.

@app.before_request
def create_session():
    """
    Перед кожним запитом, створюємо нову сесію 
    і зберігаємо її у глобальному 'g' об'єкті Flask.
    """
    # 'g' - це "глобальний" об'єкт, унікальний для кожного запиту
    g.session = SessionLocal()

@app.teardown_appcontext
def shutdown_session(exception=None):
    """
    Після кожного запиту (навіть з помилкою), 
    ми закриваємо сесію, щоб повернути її у "пул".
    """
    session = g.pop('session', None)
    if session is not None:
        # Це повертає сесію у 'pool', готове до наступного запиту
        SessionLocal.remove() 

# --- 4. Реєстрація всіх "Контролерів" ---
# Тут ми кажемо Flask'у: "Використовуй всі ці маршрути"
app.register_blueprint(artist_bp)
app.register_blueprint(user_bp)
app.register_blueprint(song_bp)
app.register_blueprint(album_bp)
app.register_blueprint(playlist_bp)
app.register_blueprint(label_bp)

# --- 5. (БЛОК init-db ВИДАЛЕНО) ---
# Ми підключаємось до готової БД.

# --- 6. Головний маршрут для перевірки ---
@app.route('/')
def hello():
    """ [GET] / - Просто для перевірки, що сервер живий """
    return jsonify({
        'message': 'Привіт! Твій Spotify API працює!',
        'docs': 'Використовуй Postman для тестування ендпоінтів, наприклад /artists'
    })


# --- 7. Запуск сервера ---
if __name__ == '__main__':
    # 'debug=True' автоматично перезавантажує сервер при змінах
    # 'port' береться з .env файлу, або 5000 за замовчуванням
    app.run(debug=True, port=int(os.getenv("PORT", 5000)))