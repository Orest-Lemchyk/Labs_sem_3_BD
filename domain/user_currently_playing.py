# domain/user_currently_playing.py
from sqlalchemy import Column, Integer, String, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base

class UserCurrentlyPlaying(Base):
    __tablename__ = 'user_currently_playing'
    
    # user_id тут одночасно і Primary Key, і Foreign Key
    user_id = Column(Integer, ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)
    song_id = Column(Integer, ForeignKey('songs.song_id', ondelete="SET NULL"))
    started_at = Column(DATETIME, server_default=func.now())
    
    # Зв'язок M:1 (до юзера)
    user = relationship("User", back_populates="currently_playing")
    
    # Зв'язок M:1 (до пісні)
    # Ми не додаємо 'back_populates' у 'Song', бо навряд чи нам знадобиться
    # діставати з пісні всіх юзерів, які її зараз слухають.
    song = relationship("Song")

    def to_dict(self):
        """ Перетворює об'єкт на словник для JSON. """
        return {
            'user_id': self.user_id,
            'song_id': self.song_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            # Можемо безпечно додати пісню (це не викличе цикл)
            'song': self.song.to_dict() if self.song else None
        }