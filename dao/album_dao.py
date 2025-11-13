# dao/album_dao.py
from dao.base_dao import BaseDAO
from domain.album import Album

class AlbumDAO(BaseDAO):
    """
    Data Access Object for Album entity.
    """
    _model = Album

    def __init__(self, session):
        self._session = session

    def find_by_title(self, title: str):
        """
        Знаходить альбоми за назвою.
        """
        return self._session.query(self._model).filter_by(title=title).all()

    def find_songs(self, album_id: int):
        """
        (Запит M:1) Знаходить всі пісні в цьому альбомі.
        """
        from domain.song import Song
        return self._session.query(Song).filter_by(album_id=album_id).all()
        
        # Альтернативний шлях через 'relationship', якщо він завантажений:
        # album = self.find_by_id(album_id)
        # return album.songs if album else []

    def find_by_label_id(self, label_id: int):
        """
        Знаходить всі альбоми, випущені певним лейблом.
        """
        return self._session.query(self._model).filter_by(label_id=label_id).all()