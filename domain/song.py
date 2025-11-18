# domain/song.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import YEAR
from sqlalchemy.orm import relationship
from config.db import Base
from .associations import song_artists_table, playlist_songs_table

class Song(Base):
    __tablename__ = 'songs'
    
    song_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    duration_sec = Column(Integer)
    release_year = Column(YEAR)
    album_id = Column(Integer, ForeignKey('albums.album_id', ondelete="SET NULL"))
    
    album = relationship("Album", back_populates="songs") 
    artists = relationship("Artist", secondary=song_artists_table, back_populates="songs")
    playlists = relationship("Playlist", secondary=playlist_songs_table, back_populates="songs")

    def to_dict(self):
        """
        Перетворює об'єкт Song на словник, 
        ВКЛЮЧАЮЧИ список артистів.
        """
        return {
            'song_id': self.song_id,
            'title': self.title,
            'duration_sec': self.duration_sec,
            'release_year': self.release_year,
            'album_id': self.album_id,
            
            # --- ОНОВЛЕНО ---
            # 'self.artists' вже будуть завантажені завдяки 'joinedload'
            # Ми викликаємо artist.to_dict(include_songs=False),
            # щоб уникнути нескінченного циклу (Song -> Artist -> Song...)
            'artists': [artist.to_dict(include_songs=False) for artist in self.artists]
            # --- КІНЕЦЬ ОНОВЛЕННЯ ---
        }