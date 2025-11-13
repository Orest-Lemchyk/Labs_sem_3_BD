# domain/playlist.py
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base
from .associations import playlist_songs_table

class Playlist(Base):
    __tablename__ = 'playlists'
    
    playlist_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DATETIME, server_default=func.now())
    
    # Зв'язок M:1 (Багато плейлистів -> Один юзер)
    user = relationship("User", back_populates="playlists")
    
    # Зв'язок M:M (Багато плейлистів -> Багато пісень)
    songs = relationship("Song", secondary=playlist_songs_table, back_populates="playlists")

    def to_dict(self):
        """ Перетворює об'єкт Playlist на словник для JSON. """
        return {
            'playlist_id': self.playlist_id,
            'user_id': self.user_id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None
            # 'user' та 'songs' не додаємо, щоб уникнути циклів
        }