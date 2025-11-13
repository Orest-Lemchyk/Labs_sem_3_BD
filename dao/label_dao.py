# dao/label_dao.py
from dao.base_dao import BaseDAO
from domain.label import Label

class LabelDAO(BaseDAO):
    """
    Data Access Object for Label entity.
    """
    _model = Label

    def __init__(self, session):
        self._session = session

    def find_by_name(self, name: str) -> Label:
        """
        Знаходить лейбл за назвою.
        """
        return self._session.query(self._model).filter_by(name=name).first()

    def find_albums(self, label_id: int):
        """
        (Запит M:1) Знаходить всі альбоми цього лейблу.
        """
        from domain.album import Album
        return self._session.query(Album).filter_by(label_id=label_id).all()