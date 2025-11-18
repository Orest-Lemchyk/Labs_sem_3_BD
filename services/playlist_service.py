# services/playlist_service.py
from dao.playlist_dao import PlaylistDAO
from dao.song_dao import SongDAO 
from domain.playlist import Playlist # <-- Імпортуємо модель

class PlaylistService:
    """
    Шар бізнес-логіки для Плейлистів.
    """
    
    def __init__(self, session):
        self.playlist_dao = PlaylistDAO(session)
        self.song_dao = SongDAO(session) # Для M:M
        self._session = session # Для .commit()

    def get_all_playlists(self):
        return self.playlist_dao.find_all()

    def get_playlist_by_id(self, playlist_id: int):
        return self.playlist_dao.find_by_id(playlist_id)

    def create_playlist(self, data: dict):
        # 'user_id' і 'name' мають бути в 'data'
        
        # Виправлення: Створюємо ОБ'ЄКТ Playlist
        new_playlist_obj = Playlist(**data)
        return self.playlist_dao.create(new_playlist_obj)

    def update_playlist(self, playlist_id: int, data: dict):
        if 'name' in data:
            return self.playlist_dao.update(playlist_id, {'name': data['name']})
        return self.playlist_dao.find_by_id(playlist_id)

    def delete_playlist(self, playlist_id: int):
        return self.playlist_dao.delete(playlist_id)
    
    # --- Методи для зв'язків (з лаби) ---
    
    def get_playlist_songs(self, playlist_id: int):
        """ (M:M) Отримати всі пісні плейлиста """
        return self.playlist_dao.find_songs(playlist_id)
    
    def add_song_to_playlist(self, playlist_id: int, song_id: int):
        """
        (M:M) Додає пісню до плейлиста.
        """
        playlist = self.playlist_dao.find_by_id(playlist_id)
        song = self.song_dao.find_by_id(song_id)
        
        if not playlist or not song:
            raise ValueError("Плейлист або пісня не знайдені.")
            
        if song in playlist.songs:
            raise ValueError("Пісня вже є у цьому плейлисті.")
            
        playlist.songs.append(song)
        self._session.commit()
        return playlist

    def remove_song_from_playlist(self, playlist_id: int, song_id: int):
        """
        (M:M) Видаляє пісню з плейлиста.
        """
        playlist = self.playlist_dao.find_by_id(playlist_id)
        song = self.song_dao.find_by_id(song_id)
        
        if not playlist or not song:
            raise ValueError("Плейлист або пісня не знайдені.")
        
        if song not in playlist.songs:
            raise ValueError("Пісні немає у цьому плейлисті.")
            
        playlist.songs.remove(song)
        self._session.commit()
        return playlist