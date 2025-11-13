# dao/song_dao.py
from dao.base_dao import BaseDAO
from domain.song import Song

class SongDAO(BaseDAO):
    """
    Data Access Object for Song entity.
    """
    _model = Song

    def __init__(self, session):
        self._session = session

    def find_by_title(self, title: str):
        """
        Знаходить всі пісні з такою назвою.
        """
        return self._session.query(self._model).filter_by(title=title).all()

    def find_by_album_id(self, album_id: int):
        """
        (Запит M:1) Знаходить всі пісні з конкретного альбому.
        """
        return self._session.query(self._model).filter_by(album_id=album_id).all()

    def find_artists(self, song_id: int):
        """
        (Запит M:M) Знаходить всіх артистів цієї пісні.
        """
        song = self.find_by_id(song_id)
        if song:
            return song.artists
        return []