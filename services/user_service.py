# services/user_service.py
from dao.user_dao import UserDAO
# (Тут ми можемо імпортувати інші DAO, якщо потрібно,
# наприклад, PlaylistDAO, щоб створити плейлист за замовчуванням)

class UserService:
    """
    Шар бізнес-логіки для Юзерів.
    """
    
    def __init__(self, session):
        self.user_dao = UserDAO(session)

    def get_all_users(self):
        return self.user_dao.find_all()

    def get_user_by_id(self, user_id: int):
        return self.user_dao.find_by_id(user_id)

    def create_user(self, data: dict):
        """
        Створює нового юзера з перевірками.
        """
        # **Приклад бізнес-логіки**
        if self.user_dao.find_by_username(data['username']):
            raise ValueError(f"Юзер з ім'ям '{data['username']}' вже існує.")
        if self.user_dao.find_by_email(data['email']):
            raise ValueError(f"Юзер з email '{data['email']}' вже існує.")
            
        # Тут має бути хешування пароля!
        # data['password_hash'] = hash_password(data['password'])
        # (поки що ми просто приймаємо 'password_hash' з 'data')

        return self.user_dao.create(data)

    def update_user(self, user_id: int, data: dict):
        """
        Оновлює юзера.
        """
        # **Приклад бізнес-логіки**
        # Не дозволяємо змінювати username або email на вже зайнятий
        if 'username' in data and self.user_dao.find_by_username(data['username']):
             raise ValueError(f"Юзер з ім'ям '{data['username']}' вже існує.")
        if 'email' in data and self.user_dao.find_by_email(data['email']):
            raise ValueError(f"Юзер з email '{data['email']}' вже існує.")

        return self.user_dao.update(user_id, data)

    def delete_user(self, user_id: int):
        return self.user_dao.delete(user_id)

    # --- Методи для зв'язків (з лаби) ---

    def get_user_playlists(self, user_id: int):
        """ (M:1) Отримати всі плейлисти юзера """
        return self.user_dao.find_playlists(user_id)

    def get_user_followers(self, user_id: int):
        """ (M:M) Отримати підписників юзера """
        return self.user_dao.find_followers(user_id)
    
    def get_user_following(self, user_id: int):
        """ (M:M) Отримати тих, на кого підписаний юзер """
        return self.user_dao.find_following(user_id)