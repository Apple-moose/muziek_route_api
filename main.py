from typing import List
from fastapi import Depends, FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from app import songs, users, database, schemas, songs, auth
from app.deps import get_current_user, is_user_admin

load_dotenv()

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/docslogin",  # also in deps.py!
    # tokenUrl="/auth/login", 

    scheme_name="JWT"
)


#-o-o-o-o-o-o-o-o-o-o-o-o- USER'S -o-o-o-o-o-o-o-o-o-o-o-o-o--oo-o-o-o-o-o-o-o-o-o-


# sign up users
@app.post("/auth/signup", response_model=schemas.UserBase)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    return users.create_user(db, user=user)


# Create server Administrator
@app.post("/auth/admin", response_model=schemas.UserBase)
def create_admin(
    user: schemas.AdminCreate, 
    db: Session = Depends(get_db)
):
    return users.create_admin(db, user=user)

# Login
@app.post("/auth/login", response_model=schemas.Token)
def login_user(
    user: schemas.UserCredentials,
    db: Session = Depends(get_db)
):
    return users.login_user(db, user=user)


# Login at /docs
@app.post("/docslogin", response_model=schemas.Token)
def login_with_form_data(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return users.docs_login_user(db, user=user)


# get user's profile
@app.get("/auth/me", response_model=schemas.User)
def get_my_user_profile(
    user: schemas.UserBase = Depends(get_current_user),
    db: Session = Depends(get_db),
    ):
    my_profile = users.get_user(
        db, 
        user_id=user.id)
    return my_profile 


#Get user profile by id
@app.get("/auth/{id}", response_model=schemas.User)
def get_user_by_id(
    id: int,
    user: schemas.UserBase = Depends(get_current_user),
    db: Session = Depends(get_db)):
    admin = is_user_admin(db, user_id=user.id)
    results = users.get_user_by_id(db, user_id=id)
    if admin is None:
        raise HTTPException(status_code=404, detail="You are not an Administratore!!!")
    if results is None:
        raise HTTPException(status_code=404, detail="No user found!!")
    return results


#-o-o-o-o-o-o-o-o-o-o-o-o- SONGS -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-


# get songs list
@app.get("/songs", response_model=List[schemas.Song])
def read_songs(
    skip: int = 0, limit: int = 20,
    db: Session = Depends(get_db)):
    results = songs.get_songs(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results


# Get song by Id
# @app.get("/songs/{prod_id}", response_model=schemas.Song)
# def read_song(
#     prod_id: int,
#     db: Session = Depends(get_db)):
#     results = songs.get_song_by_id(db, prod_id=prod_id)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


#GET songs by category's name
# @app.get("/songs/category/name:{category_name}", response_model=List[schemas.Song])
# def get_songs_list_by_category_name(
#     category_name: str,
#     db: Session = Depends(get_db)):
#     categoryId = songs.find_song_id_from_name(db, cat_name=category_name)
#     results = songs.get_songs_list_by_category_id(db, cat_id=categoryId)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


#GET songs by category's Id
# @app.get("/songs/category/categoryId:{category_id}", response_model=List[schemas.song])
# def songs_list_by_categoryId(
#     category_id: int,
#     db: Session = Depends(get_db)):
#     results = songs.get_songs_list_by_category_id(db, cat_id=category_id)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


# # create a new song profile
# @app.post("/song", response_model=schemas.song)
# def write_a_new_song(
#     song: schemas.songCreate, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     admin = is_user_admin(db, user_id=user.id)
#     if admin is None:
#         raise HTTPException(status_code=404, detail="You are not an Administrator!!!")
#     return songs.create_song(db, song=song)


# Update a song by id
# @app.post("/song/{id}", response_model=schemas.song)
# async def update_song(
#     id: int,
#     song: schemas.songUpdate, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     check_song = songs.get_song_by_id(db, prod_id=id)
#     admin = is_user_admin(db, user_id=user.id)

#     if check_song is None:
#         raise HTTPException(status_code=404, detail="song not found")
#     if admin is None:
#         raise HTTPException(status_code=404, detail="You are not an Administratore!!!")
#     else:
#         return songs.update_song(
#             db, 
#             pro_id=id, 
#             song=song)

# Remove song by id
# @app.delete("/song/{id}", response_model=schemas.song)
# def remove_song(
#     id: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     admin = is_user_admin(db, user_id=user.id)
#     if admin is None:
#         raise HTTPException(status_code=404, detail="You are not an Administratore!!!")

#     return songs.delete_song(db, pro_id=id)


#-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o CATEGORY  -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-


# Get Categories list
# @app.get("/categories", response_model=List[schemas.Category])
# def read_categories(
#     skip: int = 0, limit: int = 20,
#     db: Session = Depends(get_db)):
#     results = categories.get_categories(db, skip=skip, limit=limit)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


# create a category
# @app.post("/categories", response_model=schemas.Category)
# def create_category(
#     category: schemas.CategoryCreate, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     admin = is_user_admin(db, user_id=user.id)
#     if admin is None:
#         raise HTTPException(status_code=404, detail="You are not an Administratore!!!")
#     return categories.create_category(db, cat=category)


# # update category by id
# @app.post("/categories/{id}", response_model=schemas.Category)
# async def update_category(
#     id: int,
#     category: schemas.CategoryUpdate, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     check_category = categories.get_category(db, cat_id=id)
#     admin = is_user_admin(db, user_id=user.id)

#     if check_category is None:
#         raise HTTPException(status_code=404, detail="Category not found")
#     if admin is None:
#         raise HTTPException(status_code=404, detail="You are not an Administratore!!!")
#     else:
#         return categories.update_category(
#             db, 
#             cat_id=id, 
#             category=category)


#-o-o-o-o-o-o-o-o-o-o-o-o-o-op-  REVIEWS  -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-


# Get reviews by songId
# @app.get("/reviews/songId:{prod_id}", response_model=List[schemas.Review])
# def get_reviews_by_song_id(
#     prod_id: int,
#     skip: int = 0, limit: int = 20,
#     db: Session = Depends(get_db),

# ):
#     results = reviews.get_reviews_by_song_id(db, prod_id=prod_id, skip=skip, limit=limit)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No lists found")
#     return results


# get reviews from inlogged user
# @app.get("/reviews/me", response_model=List[schemas.Review])
# def get_my_reviews(
#     user: schemas.UserBase = Depends(get_current_user),
#     skip: int = 0, limit: int = 20,
#     db: Session = Depends(get_db),

# ):
#     results = reviews.get_users_reviews(
#         db, 
#         user_id=user.id, 
#         skip=skip, limit=limit)
#     if results is None:
#         raise HTTPException(status_code=404, detail="No reviews found")
#     return results


# update review by id
# @app.post("/review/update:{id}", response_model=schemas.Review)
# async def update_my_review(
#     id: int,
#     updated_review: schemas.ReviewUpdate, 
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     check_review = reviews.get_review(db, rev_id=id, user_id=user.id),
#     print(f"Received update for review {id} with data: {user.id}")

#     if check_review is None:
#         raise HTTPException(status_code=404, detail="Review not found")
#     else:
#         return reviews.update_review(
#             db, 
#             rev_id=id, 
#             review=updated_review)


# Create a Review as user
# @app.post("/review/{prodId}", response_model=schemas.ReviewCreate)
# def write_my_review(
#     rev: schemas.ReviewCreate, 
#     prodId: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     return reviews.create_review(
#         db, 
#         user_id=user.id, 
#         prod_id=prodId, 
#         author=user.firstname, 
#         user_imgUrl=user.imageUrl, 
#         rev=rev)

    
# Delete review by id
# @app.delete("/review/{id}", response_model=schemas.Review)
# def remove_my_review(
#     id: int,
#     user: schemas.UserBase = Depends(get_current_user),
#     db: Session = Depends(get_db)
# ):
#     return reviews.delete_review(db, rev_id=id, user_id=user.id)





@app.get("/healthz", response_model=schemas.Healthz)
def healthz():
    return {"status": "ok"}


