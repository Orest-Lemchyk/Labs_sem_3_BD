# services/song_service.py
from dao.song_dao import SongDAO
from dao.artist_dao import ArtistDAO 
from domain.song import Song # <-- Імпортуємо модель

class SongService:
    """
    Шар бізнес-логіки для Пісень.
    """
    
    def __init__(self, session):
        self.song_dao = SongDAO(session)
        self.artist_dao = ArtistDAO(session) # Потрібен для M:M логіки
        self._session = session # Потрібен для .commit() у M:M

    def get_all_songs(self):
        return self.song_dao.find_all()

    def get_song_by_id(self, song_id: int):
        return self.song_dao.find_by_id(song_id)

    def create_song(self, data: dict):
        existing = self.song_dao.find_by_title(data['title'])
        for song in existing:
            if song.album_id == data.get('album_id'):
                raise ValueError(f"Пісня '{data['title']}' вже існує в цьому альбомі.")
        
        # Виправлення: Створюємо ОБ'ЄКТ Song
        new_song_obj = Song(**data)
        return self.song_dao.create(new_song_obj)

    def update_song(self, song_id: int, data: dict):
        return self.song_dao.update(song_id, data)

    def delete_song(self, song_id: int):
        return self.song_dao.delete(song_id)
    
    # --- Методи для зв'язків (з лаби) ---
    
    def get_song_artists(self, song_id: int):
        """ (M:M) Отримати артистів пісні """
        return self.song_dao.find_artists(song_id)
    
    def add_artist_to_song(self, song_id: int, artist_id: int):
        """
        (M:M) Додає артиста до пісні.
        """
        song = self.song_dao.find_by_id(song_id)
        artist = self.artist_dao.find_by_id(artist_id)
        
        if not song or not artist:
            raise ValueError("Пісня або артист не знайдені.")
            
        if artist in song.artists:
            raise ValueError("Артист вже доданий до цієї пісні.")
            
        song.artists.append(artist)
        self._session.commit()
        return song