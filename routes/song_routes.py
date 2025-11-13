# routes/song_routes.py
from flask import Blueprint, request, jsonify, g
from services.song_service import SongService
from .utils import serialize_list

song_bp = Blueprint('songs', __name__, url_prefix='/songs')

@song_bp.route('/', methods=['GET'])
def get_songs():
    """ [GET] /songs - Отримати всі пісні """
    service = SongService(g.session)
    songs = service.get_all_songs()
    return serialize_list(songs)

@song_bp.route('/<int:song_id>', methods=['GET'])
def get_song(song_id):
    """ [GET] /songs/1 - Отримати пісню """
    service = SongService(g.session)
    song = service.get_song_by_id(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404
    return jsonify(song.to_dict())

@song_bp.route('/', methods=['POST'])
def create_song():
    """ [POST] /songs - Створити пісню """
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return jsonify({'error': 'Missing title'}), 400
        
        service = SongService(g.session)
        new_song = service.create_song(data)
        return jsonify(new_song.to_dict()), 201
    except ValueError as e: # Помилка (пісня вже існує)
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@song_bp.route('/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    """ [PUT] /songs/1 - Оновити пісню """
    service = SongService(g.session)
    data = request.get_json()
    updated_song = service.update_song(song_id, data)
    if not updated_song:
        return jsonify({'error': 'Song not found'}), 404
    return jsonify(updated_song.to_dict())

@song_bp.route('/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    """ [DELETE] /songs/1 - Видалити пісню """
    service = SongService(g.session)
    if not service.delete_song(song_id):
        return jsonify({'error': 'Song not found'}), 404
    return '', 204

# --- Маршрути для зв'язків (з лаби) ---

@song_bp.route('/<int:song_id>/artists', methods=['GET'])
def get_song_artists(song_id):
    """ [GET] /songs/1/artists - Отримати артистів пісні (M:M) """
    service = SongService(g.session)
    artists = service.get_song_artists(song_id)
    if artists is None:
        return jsonify({'error': 'Song not found'}), 404
    return serialize_list(artists)

@song_bp.route('/<int:song_id>/artists', methods=['POST'])
def add_artist_to_song(song_id):
    """ [POST] /songs/1/artists - Додати артиста до пісні (M:M) """
    try:
        data = request.get_json()
        if 'artist_id' not in data:
            return jsonify({'error': 'Missing artist_id'}), 400
        
        service = SongService(g.session)
        song = service.add_artist_to_song(song_id, data['artist_id'])
        return jsonify(song.to_dict())
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500