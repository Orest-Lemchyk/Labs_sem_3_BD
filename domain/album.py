# domain/album.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.mysql import YEAR
from sqlalchemy.orm import relationship
from config.db import Base

class Album(Base):
    __tablename__ = 'albums'
    
    album_id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    release_year = Column(YEAR)
    label_id = Column(Integer, ForeignKey('labels.label_id', ondelete="SET NULL"))
    
    # Зв'язок M:1 (Багато альбомів -> Один лейбл)
    label = relationship("Label", back_populates="albums")
    
    # Зв'язок 1:M (Один альбом -> Багато пісень)
    songs = relationship("Song", back_populates="album")

    def to_dict(self):
        """ Перетворює об'єкт Album на словник для JSON. """
        return {
            'album_id': self.album_id,
            'title': self.title,
            'release_year': self.release_year,
            'label_id': self.label_id,
            # Додаємо 'label', якщо він завантажений (це не викличе цикл)
            'label': self.label.to_dict() if self.label else None
            # 'songs' не додаємо, щоб уникнути циклу (Song->Album->Song...)
        }