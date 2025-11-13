# routes/label_routes.py
from flask import Blueprint, request, jsonify, g
from services.label_service import LabelService
from .utils import serialize_list

label_bp = Blueprint('labels', __name__, url_prefix='/labels')

@label_bp.route('/', methods=['GET'])
def get_labels():
    """ [GET] /labels - Отримати всі лейбли """
    service = LabelService(g.session)
    labels = service.get_all_labels()
    return serialize_list(labels)

@label_bp.route('/<int:label_id>', methods=['GET'])
def get_label(label_id):
    """ [GET] /labels/1 - Отримати лейбл """
    service = LabelService(g.session)
    label = service.get_label_by_id(label_id)
    if not label:
        return jsonify({'error': 'Label not found'}), 404
    return jsonify(label.to_dict())

@label_bp.route('/', methods=['POST'])
def create_label():
    """ [POST] /labels - Створити лейбл """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing name'}), 400
        
        service = LabelService(g.session)
        new_label = service.create_label(data)
        return jsonify(new_label.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@label_bp.route('/<int:label_id>', methods=['PUT'])
def update_label(label_id):
    """ [PUT] /labels/1 - Оновити лейбл """
    data = request.get_json()
    service = LabelService(g.session)
    updated_label = service.update_label(label_id, data)
    if not updated_label:
        return jsonify({'error': 'Label not found'}), 404
    return jsonify(updated_label.to_dict())

@label_bp.route('/<int:label_id>', methods=['DELETE'])
def delete_label(label_id):
    """ [DELETE] /labels/1 - Видалити лейбл """
    service = LabelService(g.session)
    if not service.delete_label(label_id):
        return jsonify({'error': 'Label not found'}), 404
    return '', 204

# --- Маршрути для зв'язків (з лаби) ---

@label_bp.route('/<int:label_id>/albums', methods=['GET'])
def get_label_albums(label_id):
    """ [GET] /labels/1/albums - Отримати альбоми лейблу (M:1) """
    service = LabelService(g.session)
    albums = service.get_label_albums(label_id)
    if albums is None:
        return jsonify({'error': 'Label not found'}), 404
    return serialize_list(albums)