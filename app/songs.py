from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from sqlalchemy.orm import joinedload

# get votes
def get_votes(db: Session):
    users =  users = db.query(models.User)\
        .options(joinedload(models.User.fav_songs), joinedload(models.User.hated_songs))\
        .all()
    all_votes = []

    for user in users:
        if user.show_no is not None:

            for song in user.fav_songs:
                favs = schemas.Votes(
                    show_no=user.show_no, 
                    user_id=user.id,
                    username=user.username,
                    song_id=song.id,
                    title=song.title,
                    artist=song.artist,
                    like=1,
                    dislike=0
                )
                all_votes.append(favs)

            for song in user.hated_songs:
                hates = schemas.Votes(
                    show_no=user.show_no,  
                    user_id=user.id,
                    username=user.username,
                    song_id=song.id,
                    title=song.title,
                    artist=song.artist,
                    like=0,
                    dislike=1
                )
                all_votes.append(hates)

    return all_votes


# get songs
def get_songs(db: Session, skip: int = 0, limit: int = 60):
    songs = db.query(models.Song).offset(skip).limit(limit).all()
    return songs

# Like a Song
def like_song(db: Session, song_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    
    if not user or not song:
        return {
            "message": "User or Song not found!"
        }
    # Append the song to the user's fav_songs
    user.fav_songs.append(song)
    db.commit()
    return {
        "user_id": user_id,
        "song_id": song_id,
        "message": "Song liked successfully!"
    }

#  Like a Song
def dislike_song(db: Session, song_id: int, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    song = db.query(models.Song).filter(models.Song.id == song_id).first()
    
    if not user or not song:
        return {
            "message": "User or Song not found!"
        }
    # Append the song to the user's hated_songs
    user.hated_songs.append(song)
    db.commit()
    return {
        "user_id": user_id,
        "song_id": song_id,
        "message": "Song disliked successfully!"
    }

def reset_votes(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return {
            "message": "User not found!"
        }
    user.hated_songs.clear()
    user.fav_songs.clear()
    db.commit()
    return user
