from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas


# get songs
# def get_songs(db: Session, skip: int = 0, limit: int = 20):
#     songs = db.query(models.Song).offset(skip).limit(limit).all()
#     return songs


# get one Song by id
# def get_song_by_id(db: Session, prod_id: int):
#     Song = db.query(models.Song).filter(
#     models.Song.id == prod_id).first()
#     return Song


# get songs by category's name (func.lower for iLike sql function!!)
# def find_song_id_from_name(db: Session, cat_name: str) -> int:
#     category = db.query(models.Category).filter(
#     func.lower(models.Category.name) == func.lower(cat_name)).first()
    
#     if category is None:
#         raise ValueError(f"No category found with name {cat_name}")
    
#     cat_id = category.id
#     return cat_id


# get songs by categoryId
# def get_songs_list_by_category_id(
#     db: Session, 
#     cat_id: int,
#     skip: int = 0,
#     limit: int = 20
#     ):
#     songs = db.query(models.Song).filter(
#     models.Song.categoryId == cat_id
#     ).offset(skip).limit(limit).all()
#     return songs


#create Song
# def create_song(db: Session, Song: schemas.songCreate):
#     db_pro = models.Song(**Song.dict())
#     db.add(db_pro)
#     db.commit()
#     db.refresh(db_pro)
#     return db_pro


#Update Song
# def update_song(
#         db: Session, 
#         Song: schemas.songUpdate, 
#         pro_id: int):
#     db_pro= db.query(models.Song).filter(
#     models.Song.id == pro_id).first()
#     updated_fields = Song.model_dump(exclude_unset=True)
#     for key, value in updated_fields.items():
#         setattr(db_pro, key, value)  
#     db.commit()
#     db.refresh(db_pro)
#     return db_pro

#delete Song
# def delete_song(db: Session, pro_id: int):
#     prod = db.query(models.Song).filter(
#     models.Song.id == pro_id).first()
#     db.delete(prod)
#     db.commit()
#     return prod

