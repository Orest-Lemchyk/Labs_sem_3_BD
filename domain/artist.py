# domain/artist.py
from sqlalchemy import Column, Integer, String, TEXT, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base
# Імпортуємо нашу M:M таблицю
from .associations import song_artists_table

class Artist(Base):
    __tablename__ = 'artists'
    
    artist_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    bio = Column(TEXT)
    created_at = Column(DATETIME, server_default=func.now())
    
    # Зв'язок M:M (Багато артистів -> Багато пісень)
    # "secondary" вказує на M:M таблицю
    songs = relationship("Song", secondary=song_artists_table, back_populates="artists")

    def to_dict(self):
        """ Перетворює об'єкт Artist на словник для JSON. """
        return {
            'artist_id': self.artist_id,
            'name': self.name,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None
            # Ми НЕ додаємо 'songs' сюди, щоб уникнути нескінченного циклу
        }