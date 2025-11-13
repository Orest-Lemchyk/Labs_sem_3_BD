# domain/associations.py
from sqlalchemy import Column, Integer, ForeignKey, DATETIME, Table
from sqlalchemy.sql import func
from config.db import Base # Імпортуємо наш Base

# M:M: Songs <-> Artists
song_artists_table = Table('song_artists', Base.metadata,
    Column('song_id', Integer, ForeignKey('songs.song_id', ondelete="CASCADE"), primary_key=True),
    Column('artist_id', Integer, ForeignKey('artists.artist_id', ondelete="CASCADE"), primary_key=True)
)

# M:M: Playlists <-> Songs
playlist_songs_table = Table('playlist_songs', Base.metadata,
    Column('playlist_id', Integer, ForeignKey('playlists.playlist_id', ondelete="CASCADE"), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.song_id', ondelete="CASCADE"), primary_key=True),
    Column('added_at', DATETIME, server_default=func.now())
)

# M:M: Users <-> Users (Followers)
user_followers_table = Table('user_followers', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True),
    Column('follower_id', Integer, ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True),
    Column('followed_at', DATETIME, server_default=func.now())
)