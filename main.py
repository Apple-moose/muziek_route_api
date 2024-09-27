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
@app.post("/signup", response_model=schemas.UserBase)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
):
    return users.create_user(db, user=user)

@app.delete("/signup/{id}", response_model=schemas.UserBase)
def remove_user(
    id: int,
    # user: schemas.UserBase,
    db: Session = Depends(get_db)
):
    return users.delete_user(db, user_id=id)


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
    skip: int = 0, limit: int = 60,
    db: Session = Depends(get_db)):
    results = songs.get_songs(db, skip=skip, limit=limit)
    if results is None:
        raise HTTPException(status_code=404, detail="No lists found")
    return results

#-o-o-o-o-o-o-o-o-o-o-o-o-o VOTES -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-

# Update User's Likes
@app.post("/like", response_model=schemas.Favs)
def like_song(
    song_id: int, 
    user_id: int,
    db: Session = Depends(get_db)
):
    return songs.like_song(db, song_id=song_id, user_id=user_id)

# Update User's dislike
@app.post("/dislike", response_model=schemas.Hates)
def dislike_song(
    song_id: int, 
    user_id: int,
    db: Session = Depends(get_db)
):
    return songs.dislike_song(db, song_id=song_id, user_id=user_id)

# Reset all votes from user
@app.delete("/reset/{id}", response_model=schemas.User)
def reset_votes(
    id: int,
    db: Session = Depends(get_db)
):
    return songs.reset_votes(db, user_id=id)



# For RENDER.com------------------------------------
@app.get("/healthz", response_model=schemas.Healthz)
def healthz():
    return {"status": "ok"}


