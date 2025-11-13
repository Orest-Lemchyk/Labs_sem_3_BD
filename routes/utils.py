from flask import jsonify

def serialize_list(items):
    """
    Перетворює список SQLAlchemy об'єктів на JSON-список.
    Кожен об'єкт у списку ПОВИНЕН мати метод .to_dict()
    """
    if not items:
        return jsonify([])
    # Викликаємо .to_dict() для кожного об'єкта у списку
    return jsonify([item.to_dict() for item in items])