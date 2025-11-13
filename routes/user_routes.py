# routes/user_routes.py
from flask import Blueprint, request, jsonify, g
from services.user_service import UserService
from .utils import serialize_list

user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    """ [GET] /users - Отримати всіх юзерів """
    service = UserService(g.session)
    users = service.get_all_users()
    return serialize_list(users)

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """ [GET] /users/1 - Отримати юзера за ID """
    service = UserService(g.session)
    user = service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict())

@user_bp.route('/', methods=['POST'])
def create_user():
    """ [POST] /users - Створити нового юзера """
    try:
        data = request.get_json()
        if not data or 'username' not in data or 'email' not in data or 'password_hash' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        service = UserService(g.session)
        new_user = service.create_user(data)
        return jsonify(new_user.to_dict()), 201
    except ValueError as e: # Помилки (юзер існує)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """ [PUT] /users/1 - Оновити юзера """
    try:
        data = request.get_json()
        service = UserService(g.session)
        updated_user = service.update_user(user_id, data)
        if not updated_user:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(updated_user.to_dict())
    except ValueError as e: # Помилки (email зайнятий)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """ [DELETE] /users/1 - Видалити юзера """
    service = UserService(g.session)
    if not service.delete_user(user_id):
        return jsonify({'error': 'User not found'}), 404
    return '', 204

# --- Маршрути для зв'язків (з лаби) ---

@user_bp.route('/<int:user_id>/playlists', methods=['GET'])
def get_user_playlists(user_id):
    """ [GET] /users/1/playlists - Отримати плейлисти юзера (M:1) """
    service = UserService(g.session)
    playlists = service.get_user_playlists(user_id)
    return serialize_list(playlists)

@user_bp.route('/<int:user_id>/followers', methods=['GET'])
def get_user_followers(user_id):
    """ [GET] /users/1/followers - Отримати підписників юзера (M:M) """
    service = UserService(g.session)
    users = service.get_user_followers(user_id)
    return serialize_list(users)

@user_bp.route('/<int:user_id>/following', methods=['GET'])
def get_user_following(user_id):
    """ [GET] /users/1/following - Отримати тих, на кого юзер підписаний (M:M) """
    service = UserService(g.session)
    users = service.get_user_following(user_id)
    return serialize_list(users)