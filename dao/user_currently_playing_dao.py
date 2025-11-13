# dao/user_currently_playing_dao.py
from dao.base_dao import BaseDAO
from domain.user_currently_playing import UserCurrentlyPlaying

class UserCurrentlyPlayingDAO(BaseDAO):
    """
    Data Access Object for UserCurrentlyPlaying entity.
    """
    _model = UserCurrentlyPlaying

    def __init__(self, session):
        self._session = session
    
    # find_by_id(user_id) вже є у BaseDAO, оскільки user_id - це PK

    def find_by_song_id(self, song_id: int):
        """
        Знаходить всіх юзерів, які зараз слухають цю пісню.
        """
        return self._session.query(self._model).filter_by(song_id=song_id).all()