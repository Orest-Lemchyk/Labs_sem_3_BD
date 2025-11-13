from abc import ABC
from typing import List


class BaseDAO(ABC):
    """
    The common realization of Data Access class.
    """
    _model = None
    _session = None

    def find_all(self) -> List[object]:
        """
        Gets all objects from table.
        :return: list of all objects
        """
        return self._session.query(self._model).all()

    def find_by_id(self, key: int) -> object:
        """
        Gets object from database table by integer key.
        :param key: integer (PK)
        :return: object
        """
        return self._session.get(self._model, key)

    def create(self, obj: object) -> object:
        """
        Creates obj in database table.
        :param obj: object to create in database
        :return: created obj
        """
        self._session.add(obj)
        self._session.commit()
        return obj

    def create_all(self, obj_list: List[object]) -> List[object]:
        """
        Creates objects from object list.
        :param obj_list: object list to create in database
        :return: list of created object
        """
        self._session.add_all(obj_list)
        self._session.commit()
        return obj_list

    def update(self, key: int, attrs: dict) -> None:
        """
        Updates object in database table.
        :param key: integer (PK)
        :param attrs: dict of attributes to update
        """
        obj = self._session.get(self._model, key)
        if obj:
            for attr_name, attr_value in attrs.items():
                if hasattr(obj, attr_name):
                    setattr(obj, attr_name, attr_value)
            self._session.commit()

    def patch(self, key: int, field: str, value: object) -> None:
        """
        Modifies defined field of object in database table.
        :param key: integer (PK)
        :param field: field name of object
        :param value: field value of object
        """
        obj = self._session.get(self._model, key)
        if obj:
            setattr(obj, field, value)
            self._session.commit()

    def delete(self, key: int) -> None:
        """
        Deletes object from database table by integer key.
        :param key: integer (PK)
        """
        obj = self._session.get(self._model, key)
        if obj:
            self._session.delete(obj)
            try:
                self._session.commit()
            except Exception:
                self._session.rollback()
                raise

    def delete_all(self) -> None:
        """
        Deletes all objects from database table.
        """
        self._session.query(self._model).delete()
        self._session.commit()
