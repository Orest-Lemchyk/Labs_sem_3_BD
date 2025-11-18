# dao/base_dao.py
class BaseDAO:
    """
    Базовий DAO з основними CRUD-операціями.
    Ця версія ПОВЕРТАЄ результати, щоб 'routes' могли 
    коректно обробляти відповіді.
    """
    _model = None # Потрібно перевизначити у дочірніх класах

    def __init__(self, session):
        self._session = session

    def find_by_id(self, id: int):
        """
        Знаходить об'єкт за його ID.
        (Використовуємо .get() замість .query(), бо це швидше для PK)
        """
        return self._session.get(self._model, id)

    def find_all(self):
        """
        Знаходить всі об'єкти.
        """
        return self._session.query(self._model).all()

    def create(self, obj: object):
        """
        Створює новий об'єкт в БД.
        (Ми очікуємо ОБ'ЄКТ, а не dict - це виправлено у services)
        """
        try:
            self._session.add(obj)
            self._session.commit()
            self._session.refresh(obj)
            return obj
        except Exception as e:
            self._session.rollback()
            print(f"Помилка при створенні об'єкта: {e}")
            raise e 

    def update(self, id: int, data: dict):
        """
        Оновлює об'єкт за ID, використовуючи словник 'data'.
        ПОВЕРТАЄ оновлений об'єкт або None.
        """
        try:
            obj = self.find_by_id(id) # Використовуємо self.find_by_id
            if obj:
                # Оновлюємо тільки ті поля, які є в 'data'
                for key, value in data.items():
                    if hasattr(obj, key):
                        setattr(obj, key, value)
                self._session.commit()
                self._session.refresh(obj)
                return obj # <-- ПОВЕРТАЄМО ОБ'ЄКТ
            
            return None # <-- ПОВЕРТАЄМО None, ЯКЩО НЕ ЗНАЙШЛИ
        except Exception as e:
            self._session.rollback()
            print(f"Помилка при оновленні об'єкта: {e}")
            raise e

    def delete(self, id: int):
        """
        Видаляє об'єкт за ID.
        ПОВЕРТАЄ True або False.
        """
        try:
            obj = self.find_by_id(id) # Використовуємо self.find_by_id
            if obj:
                self._session.delete(obj)
                self._session.commit()
                return True # <-- ПОВЕРТАЄМО TRUE
            
            return False # <-- ПОВЕРТАЄМО FALSE, ЯКЩО НЕ ЗНАЙШЛИ
        except Exception as e:
            self._session.rollback()
            print(f"Помилка при видаленні об'єкта: {e}")
            raise e