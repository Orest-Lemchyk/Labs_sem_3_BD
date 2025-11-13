# routes/album_routes.py
from flask import Blueprint, request, jsonify, g
from services.album_service import AlbumService
from .utils import serialize_list

album_bp = Blueprint('albums', __name__, url_prefix='/albums')

@album_bp.route('/', methods=['GET'])
def get_albums():
    """ [GET] /albums - Отримати всі альбоми """
    service = AlbumService(g.session)
    albums = service.get_all_albums()
    return serialize_list(albums)

@album_bp.route('/<int:album_id>', methods=['GET'])
def get_album(album_id):
    """ [GET] /albums/1 - Отримати альбом """
    service = AlbumService(g.session)
    album = service.get_album_by_id(album_id)
    if not album:
        return jsonify({'error': 'Album not found'}), 404
    return jsonify(album.to_dict())

@album_bp.route('/', methods=['POST'])
def create_album():
    """ [POST] /albums - Створити альбом """
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Missing title'}), 400
    
    service = AlbumService(g.session)
    new_album = service.create_album(data)
    return jsonify(new_album.to_dict()), 201

@album_bp.route('/<int:album_id>', methods=['PUT'])
def update_album(album_id):
    """ [PUT] /albums/1 - Оновити альбом """
    data = request.get_json()
    service = AlbumService(g.session)
    updated_album = service.update_album(album_id, data)
    if not updated_album:
        return jsonify({'error': 'Album not found'}), 404
    return jsonify(updated_album.to_dict())

@album_bp.route('/<int:album_id>', methods=['DELETE'])
def delete_album(album_id):
    """ [DELETE] /albums/1 - Видалити альбом """
    service = AlbumService(g.session)
    if not service.delete_album(album_id):
        return jsonify({'error': 'Album not found'}), 404
    return '', 204

# --- Маршрути для зв'язків (з лаби) ---

@album_bp.route('/<int:album_id>/songs', methods=['GET'])
def get_album_songs(album_id):
    """ [GET] /albums/1/songs - Отримати пісні альбому (M:1) """
    service = AlbumService(g.session)
    songs = service.get_album_songs(album_id)
    return serialize_list(songs)