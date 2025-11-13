# routes/playlist_routes.py
from flask import Blueprint, request, jsonify, g
from services.playlist_service import PlaylistService
from .utils import serialize_list

playlist_bp = Blueprint('playlists', __name__, url_prefix='/playlists')

@playlist_bp.route('/', methods=['GET'])
def get_playlists():
    """ [GET] /playlists - Отримати всі плейлисти """
    service = PlaylistService(g.session)
    playlists = service.get_all_playlists()
    return serialize_list(playlists)

@playlist_bp.route('/<int:playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    """ [GET] /playlists/1 - Отримати плейлист """
    service = PlaylistService(g.session)
    playlist = service.get_playlist_by_id(playlist_id)
    if not playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(playlist.to_dict())

@playlist_bp.route('/', methods=['POST'])
def create_playlist():
    """ [POST] /playlists - Створити плейлист """
    data = request.get_json()
    if not data or 'name' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing name or user_id'}), 400
    
    service = PlaylistService(g.session)
    new_playlist = service.create_playlist(data)
    return jsonify(new_playlist.to_dict()), 201

@playlist_bp.route('/<int:playlist_id>', methods=['PUT'])
def update_playlist(playlist_id):
    """ [PUT] /playlists/1 - Оновити плейлист """
    data = request.get_json()
    service = PlaylistService(g.session)
    updated_playlist = service.update_playlist(playlist_id, data)
    if not updated_playlist:
        return jsonify({'error': 'Playlist not found'}), 404
    return jsonify(updated_playlist.to_dict())

@playlist_bp.route('/<int:playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    """ [DELETE] /playlists/1 - Видалити плейлист """
    service = PlaylistService(g.session)
    if not service.delete_playlist(playlist_id):
        return jsonify({'error': 'Playlist not found'}), 404
    return '', 204

# --- Маршрути для зв'язків (з лаби) ---

@playlist_bp.route('/<int:playlist_id>/songs', methods=['GET'])
def get_playlist_songs(playlist_id):
    """ [GET] /playlists/1/songs - Отримати пісні плейлиста (M:M) """
    service = PlaylistService(g.session)
    songs = service.get_playlist_songs(playlist_id)
    if songs is None:
        return jsonify({'error': 'Playlist not found'}), 404
    return serialize_list(songs)

@playlist_bp.route('/<int:playlist_id>/songs', methods=['POST'])
def add_song_to_playlist(playlist_id):
    """ [POST] /playlists/1/songs - Додати пісню до плейлиста (M:M) """
    try:
        data = request.get_json()
        if 'song_id' not in data:
            return jsonify({'error': 'Missing song_id'}), 400
        
        service = PlaylistService(g.session)
        playlist = service.add_song_to_playlist(playlist_id, data['song_id'])
        return jsonify(playlist.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@playlist_bp.route('/<int:playlist_id>/songs/<int:song_id>', methods=['DELETE'])
def remove_song_from_playlist(playlist_id, song_id):
    """ [DELETE] /playlists/1/songs/1 - Видалити пісню з плейлиста (M:M) """
    try:
        service = PlaylistService(g.session)
        playlist = service.remove_song_from_playlist(playlist_id, song_id)
        return jsonify(playlist.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500