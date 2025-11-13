# services/artist_service.py
from dao.artist_dao import ArtistDAO

class ArtistService:
    """
    Шар бізнес-логіки для Артистів.
    """
    
    def __init__(self, session):
        self.artist_dao = ArtistDAO(session)

    def get_all_artists(self):
        return self.artist_dao.find_all()

    def get_artist_by_id(self, artist_id: int):
        return self.artist_dao.find_by_id(artist_id)

    def create_artist(self, data: dict):
        """
        Створює нового артиста.
        """
        if self.artist_dao.find_by_name(data['name']):
            raise ValueError(f"Артист з ім'ям '{data['name']}' вже існує.")
        
        return self.artist_dao.create(data)

    def update_artist(self, artist_id: int, data: dict):
        return self.artist_dao.update(artist_id, data)

    def delete_artist(self, artist_id: int):
        return self.artist_dao.delete(artist_id)
    
    # --- Методи для зв'язків (з лаби) ---
    
    def get_artist_songs(self, artist_id: int):
        """ (M:M) Отримати всі пісні артиста """
        return self.artist_dao.find_songs(artist_id)