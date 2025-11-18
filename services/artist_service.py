# services/artist_service.py
from dao.artist_dao import ArtistDAO
from domain.artist import Artist # <-- Імпортуємо модель

class ArtistService:
    """
    Шар бізнес-логіки для Артистів.
    """
    
    def __init__(self, session):
        """
        Ініціалізує сервіс, приймаючи сесію з g.session.
        :param session: Сесія SQLAlchemy
        """
        self.artist_dao = ArtistDAO(session)

    def get_all_artists(self):
        return self.artist_dao.find_all()

    def get_artist_by_id(self, artist_id: int):
        return self.artist_dao.find_by_id(artist_id)

    def create_artist(self, data: dict):
        """
        Створює нового артиста.
        """
        # 1. Бізнес-логіка: Перевірка на дублікат
        if self.artist_dao.find_by_name(data['name']):
            raise ValueError(f"Артист з ім'ям '{data['name']}' вже існує.")
        
        # 2. Виправлення: Створюємо ОБ'ЄКТ Artist з 'dict'
        new_artist_obj = Artist(**data) 
        
        # 3. Передаємо ОБ'ЄКТ (а не dict) в DAO
        return self.artist_dao.create(new_artist_obj)

    def update_artist(self, artist_id: int, data: dict):
        """
        Оновлює артиста.
        (Тут 'data' - це 'dict', що очікує твій BaseDAO.update)
        """
        return self.artist_dao.update(artist_id, data)

    def delete_artist(self, artist_id: int):
        return self.artist_dao.delete(artist_id)
    
    # --- Методи для зв'язків (з лаби) ---
    
    def get_artist_songs(self, artist_id: int):
        """ (M:M) Отримати всі пісні артиста """
        return self.artist_dao.find_songs(artist_id)