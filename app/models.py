from .database import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Table, func
from sqlalchemy.orm import relationship

# Association tables
fav_association_table = Table(
    'user_favs', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True)
)

hate_association_table = Table(
    'user_hates', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('song_id', Integer, ForeignKey('songs.id'), primary_key=True)
)

# Main tables
class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False, index=True)
    artist = Column(String, nullable=False, index=True)
    
    fav_by = relationship("User", secondary=fav_association_table, back_populates="fav_songs")
    hated_by = relationship("User", secondary=hate_association_table, back_populates="hated_songs")

    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    username = Column(String, nullable=False)

    fav_songs = relationship("Song", secondary=fav_association_table, back_populates="fav_by")
    hated_songs = relationship("Song", secondary=hate_association_table, back_populates="hated_by")

    password = Column(String, nullable=True)
    show_no = Column(Integer, nullable=True)
    is_Admin = Column(Boolean, default=False)
    createdAt = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    updatedAt = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)
