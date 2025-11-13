# dao/user_dao.py
from dao.base_dao import BaseDAO
from domain.user import User

class UserDAO(BaseDAO):
    """
    Data Access Object for User entity.
    """
    _model = User

    def __init__(self, session):
        self._session = session

    def find_by_email(self, email: str) -> User:
        """
        Знаходить юзера за email.
        """
        return self._session.query(self._model).filter_by(email=email).first()

    def find_by_username(self, username: str) -> User:
        """
        Знаходить юзера за username.
        """
        return self._session.query(self._model).filter_by(username=username).first()

    # --- Приклади запитів до зв'язків (як у лабі) ---

    def find_playlists(self, user_id: int):
        """
        (Запит M:1) Знаходить всі плейлисти, що належать юзеру.
        """
        from domain.playlist import Playlist
        return self._session.query(Playlist).filter_by(user_id=user_id).all()

    def find_followers(self, user_id: int):
        """
        (Запит M:M) Знаходить всіх, хто підписаний на цього юзера.
        """
        user = self.find_by_id(user_id)
        if user:
            # Використовуємо 'relationship', який ми визначили у domain/user.py
            return user.followers
        return []

    def find_following(self, user_id: int):
        """
        (Запит M:M) Знаходить всіх, на кого підписаний цей юзер.
        """
        user = self.find_by_id(user_id)
        if user:
            # Використовуємо 'relationship'
            return user.following
        return []