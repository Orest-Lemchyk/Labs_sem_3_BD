from abc import ABC
from typing import List


class BaseController(ABC):
    """
    The common realization of controller.
    """
    _service = None

    def find_all(self) -> List[object]:
        """
        Gets all objects from table using Service layer.
        :return: list of all objects
        """
        return self._service.find_all()

    def find_by_id(self, key: int) -> object:
        """
        Gets object from database table by integer key using from Service layer.
        :param key: integer (PK)
        :return: search object
        """
        return self._service.find_by_id(key)

    def create(self, obj: object) -> object:
        """
        Creates object in database table using Service layer.
        :param obj: object to create in Database
        :return: created object
        """
        return self._service.create(obj)

    def create_all(self, obj_list: List[object]) -> List[object]:
        """
        Creates objects from object list using Service layer.
        :param obj_list: object list to create in Database
        :return: list of created object
        """
        return self._service.create_all(obj_list)

    def update(self, key: int, obj: object) -> None:
        """
        Updates object in database table using Service layer.
        :param key: integer (PK)
        :param obj: object to create in Database
        :return: created object
        """
        self._service.update(key, obj)

    def patch(self, key: int, field: str, value: object) -> None:
        """
        Modifies defined field of object in database table using Service layer.
        :param key: integer (PK)
        :param field: field name of object
        :param value: field value of object
        """
        self._service.patch(key, field, value)

    def delete(self, key: int) -> None:
        """
        Deletes object from database table by integer key from Service layer.
        :param key: integer (PK)
        """
        self._service.delete(key)

    def delete_all(self) -> None:
        """
        Deletes all objects from database table using Service layer.
        """
        self._service.delete_all()
