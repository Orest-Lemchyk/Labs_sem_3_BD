# dao/song_dao.py
from dao.base_dao import BaseDAO
from domain.song import Song
from sqlalchemy.orm import joinedload # <-- 1. Імпортуємо 'joinedload'

class SongDAO(BaseDAO):
    """
    Data Access Object for Song entity.
    """
    _model = Song

    def __init__(self, session):
        self._session = session
        
    def find_all(self):
        """
        Знаходить всі пісні, ОДРАЗУ завантажуючи
        пов'язаних артистів (щоб уникнути N+1).
        """
        # 2. Додаємо .options(joinedload(...))
        return self._session.query(self._model).options(
            joinedload(self._model.artists) 
        ).all()

    def find_by_title(self, title: str):
        return self._session.query(self._model).filter_by(title=title).all()

    def find_by_album_id(self, album_id: int):
        return self._session.query(self._model).filter_by(album_id=album_id).all()

    def find_artists(self, song_id: int):
        song = self.find_by_id(song_id)
        if song:
            return song.artists
        return []