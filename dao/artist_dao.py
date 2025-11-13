# dao/artist_dao.py
from dao.base_dao import BaseDAO
from domain.artist import Artist

class ArtistDAO(BaseDAO):
    """
    Data Access Object for Artist entity.
    """
    _model = Artist

    def __init__(self, session):
        self._session = session
    
    def find_by_name(self, name: str) -> Artist:
        """
        Знаходить артиста за ім'ям.
        """
        return self._session.query(self._model).filter_by(name=name).first()

    def find_songs(self, artist_id: int):
        """
        (Запит M:M) Знаходить всі пісні цього артиста.
        """
        artist = self.find_by_id(artist_id)
        if artist:
            # Використовуємо 'relationship' з domain/artist.py
            return artist.songs
        return []