# domain/user.py
from sqlalchemy import Column, Integer, String, DATETIME
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from config.db import Base
from .associations import user_followers_table

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DATETIME, server_default=func.now())
    
    # Зв'язок 1:M (Один юзер -> Багато плейлистів)
    playlists = relationship("Playlist", back_populates="user", cascade="all, delete")
    
    # Зв'язок 1:1 (Один юзер -> Один 'currently_playing' запис)
    currently_playing = relationship("UserCurrentlyPlaying", back_populates="user", uselist=False, cascade="all, delete")

    # Зв'язок M:M (самопосилальний)
    # 'following' - це список користувачів, на яких підписаний ЦЕЙ юзер
    following = relationship(
        "User", # Зв'язок з тим самим класом User
        secondary=user_followers_table,
        primaryjoin=(user_followers_table.c.follower_id == user_id),
        secondaryjoin=(user_followers_table.c.user_id == user_id),
        back_populates="followers"
    )
    # 'followers' - це список користувачів, які підписані на ЦЬОГО юзера
    followers = relationship(
        "User",
        secondary=user_followers_table,
        primaryjoin=(user_followers_table.c.user_id == user_id),
        secondaryjoin=(user_followers_table.c.follower_id == user_id),
        back_populates="following"
    )

    def to_dict(self):
        """ Перетворює об'єкт User на словник для JSON. """
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
            # 'password_hash' ми ніколи не повертаємо!
        }