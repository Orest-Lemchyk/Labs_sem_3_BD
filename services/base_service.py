from abc import ABC
from typing import List


class BaseService(ABC):
    """
    The common realization of the Business Layer class.
    """
    _dao = None

    def find_all(self) -> List[object]:
        """
        Gets all objects from table using Data Access layer.
        :return: list of all objects
        """
        return self._dao.find_all()

    def find_by_id(self, key: int) -> object:
        """
        Gets object from database table by integer key using from Data Access layer.
        :param key: integer (PK)
        :return: object
        """
        return self._dao.find_by_id(key)

    def create(self, obj: object) -> object:
        """
        Creates object in database table using Data Access layer.
        :param obj: object to create in Database
        :return: created object
        """
        return self._dao.create(obj)

    def create_all(self, obj_list: List[object]) -> List[object]:
        """
        Creates objects from object list using Data Access layer.
        :param obj_list: object list to create in Database
        :return: list of created object
        """
        return self._dao.create_all(obj_list)

    def update(self, key: int, obj: object):
        """
        Updates object in database table using Data Access layer.
        :param key: integer (PK)
        :param obj: object to create in Database
        :return: created object
        """
        self._dao.update(key, obj)

    def patch(self, key: int, field: str, value: object):
        """
        Modifies defined field of object in database table using Data Access layer.
        :param key: integer (PK)
        :param field: field name of object
        :param value: field value of object
        """
        self._dao.patch(key, field, value)

    def delete(self, key: int) -> None:
        """
        Deletes object from database table by integer key from Data Access layer.
        :param key: integer (PK)
        """
        self._dao.delete(key)

    def delete_all(self) -> None:
        """
        Deletes all objects from database table using Data Access layer.
        """
        self._dao.delete_all()
