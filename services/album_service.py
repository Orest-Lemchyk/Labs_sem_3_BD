# services/album_service.py
from dao.album_dao import AlbumDAO
from domain.album import Album # <-- Імпортуємо модель

class AlbumService:
    """
    Шар бізнес-логіки для Альбомів.
    """
    
    def __init__(self, session):
        self.album_dao = AlbumDAO(session)

    def get_all_albums(self):
        return self.album_dao.find_all()

    def get_album_by_id(self, album_id: int):
        return self.album_dao.find_by_id(album_id)

    def create_album(self, data: dict):
        # Виправлення: Створюємо ОБ'ЄКТ Album
        new_album_obj = Album(**data)
        return self.album_dao.create(new_album_obj)

    def update_album(self, album_id: int, data: dict):
        return self.album_dao.update(album_id, data)

    def delete_album(self, album_id: int):
        return self.album_dao.delete(album_id)
    
    # --- Методи для зв'язків (з лаби) ---
    
    def get_album_songs(self, album_id: int):
        """ (M:1) Отримати всі пісні альбому """
        return self.album_dao.find_songs(album_id)