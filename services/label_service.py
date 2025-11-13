# services/label_service.py
from dao.label_dao import LabelDAO

class LabelService:
    """
    Шар бізнес-логіки для Лейблів.
    """
    
    def __init__(self, session):
        self.label_dao = LabelDAO(session)

    def get_all_labels(self):
        return self.label_dao.find_all()

    def get_label_by_id(self, label_id: int):
        return self.label_dao.find_by_id(label_id)

    def create_label(self, data: dict):
        if self.label_dao.find_by_name(data['name']):
            raise ValueError(f"Лейбл з ім'ям '{data['name']}' вже існує.")
        return self.label_dao.create(data)

    def update_label(self, label_id: int, data: dict):
        return self.label_dao.update(label_id, data)

    def delete_label(self, label_id: int):
        return self.label_dao.delete(label_id)
    
    # --- Методи для зв'язків (з лаби) ---
    
    def get_label_albums(self, label_id: int):
        """ (M:1) Отримати всі альбоми лейблу """
        return self.label_dao.find_albums(label_id)