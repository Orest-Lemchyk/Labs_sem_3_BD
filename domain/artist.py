# domain/artist.py
from sqlalchemy import Column, Integer, String, TEXT, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base
from .associations import song_artists_table

class Artist(Base):
    __tablename__ = 'artists'
    
    artist_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    bio = Column(TEXT)
    created_at = Column(DATETIME, server_default=func.now())
    
    songs = relationship("Song", secondary=song_artists_table, back_populates="artists")
    
    # --- ОНОВЛЕНО ---
    def to_dict(self, include_songs=True): # Додаємо 'include_songs'
        """
        Перетворює об'єкт Artist на словник.
        'include_songs=False' використовується, щоб уникнути циклів.
        """
        data = {
            'artist_id': self.artist_id,
            'name': self.name,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        # За замовчуванням ми НЕ хочемо цього, 
        # але це робить наш .to_dict() гнучким
        if include_songs:
             data['songs'] = [song.to_dict() for song in self.songs]
             
        return data
    # --- КІНЕЦЬ ОНОВЛЕННЯ ---