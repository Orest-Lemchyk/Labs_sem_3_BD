# dao/playlist_dao.py
from dao.base_dao import BaseDAO
from domain.playlist import Playlist

class PlaylistDAO(BaseDAO):
    """
    Data Access Object for Playlist entity.
    """
    _model = Playlist

    def __init__(self, session):
        self._session = session

    def find_by_user_id(self, user_id: int):
        """
        (Запит M:1) Знаходить всі плейлисти юзера.
        """
        return self._session.query(self._model).filter_by(user_id=user_id).all()

    def find_by_name(self, name: str):
        """
        Знаходить плейлисти за назвою (може бути багато з однаковою назвою).
        """
        return self._session.query(self._model).filter(self._model.name.like(f"%{name}%")).all()

    def find_songs(self, playlist_id: int):
        """
        (Запит M:M) Знаходить всі пісні в цьому плейлисті.
        """
        playlist = self.find_by_id(playlist_id)
        if playlist:
            # Використовуємо 'relationship'
            return playlist.songs
        return []