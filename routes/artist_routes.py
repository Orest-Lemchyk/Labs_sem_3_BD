# routes/artist_routes.py
from flask import Blueprint, request, jsonify, g
from services.artist_service import ArtistService
from .utils import serialize_list # Наш хелпер

# 'artists' - це префікс для всіх URL (тобто /artists, /artists/1)
artist_bp = Blueprint('artists', __name__, url_prefix='/artists')

@artist_bp.route('/', methods=['GET'])
def get_artists():
    """ [GET] /artists - Отримати всіх артистів """
    try:
        # g.session створюється та закривається у app.py
        service = ArtistService(g.session) 
        artists = service.get_all_artists()
        return serialize_list(artists)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artist_bp.route('/<int:artist_id>', methods=['GET'])
def get_artist(artist_id):
    """ [GET] /artists/1 - Отримати артиста за ID """
    try:
        service = ArtistService(g.session)
        artist = service.get_artist_by_id(artist_id)
        if not artist:
            return jsonify({'error': 'Artist not found'}), 404
        return jsonify(artist.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artist_bp.route('/', methods=['POST'])
def create_artist():
    """ [POST] /artists - Створити нового артиста """
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Missing data or name'}), 400
            
        service = ArtistService(g.session)
        new_artist = service.create_artist(data)
        return jsonify(new_artist.to_dict()), 201 # 201 = Created
    except ValueError as e: # Помилка з сервісу (напр. "Артист вже існує")
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artist_bp.route('/<int:artist_id>', methods=['PUT'])
def update_artist(artist_id):
    """ [PUT] /artists/1 - Оновити артиста """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing data'}), 400
            
        service = ArtistService(g.session)
        updated_artist = service.update_artist(artist_id, data)
        if not updated_artist:
            return jsonify({'error': 'Artist not found'}), 404
        return jsonify(updated_artist.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@artist_bp.route('/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    """ [DELETE] /artists/1 - Видалити артиста """
    try:
        service = ArtistService(g.session)
        if not service.delete_artist(artist_id):
            return jsonify({'error': 'Artist not found'}), 404
        return '', 204 # 204 = No Content (успішне видалення)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Маршрути для зв'язків (з лаби) ---

@artist_bp.route('/<int:artist_id>/songs', methods=['GET'])
def get_artist_songs(artist_id):
    """ [GET] /artists/1/songs - Отримати всі пісні артиста (M:M) """
    try:
        service = ArtistService(g.session)
        songs = service.get_artist_songs(artist_id)
        if songs is None:
             return jsonify({'error': 'Artist not found'}), 404
        return serialize_list(songs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500