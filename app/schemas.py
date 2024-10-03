
from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Voting stuff
class Votes(BaseModel):
    show_no: int
    user_id: int
    username: str
    song_id: int
    title: str
    artist: str
    like: int
    dislike: int

    class Config:
        from_attributes = True 

class FavsBase(BaseModel):
    user_id: int
    song_id: int

    class Config:
        orm_mode = True

class Favs(FavsBase):
    user_id: int
    song_id: int

    class Config:
        from_attributes = True 

class HatesBase(BaseModel):
    user_id: int
    song_id: int

    class Config:
        orm_mode = True


class Hates(HatesBase):
    user_id: int
    song_id: int

    class Config:
        from_attributes = True 

# Song stuff

class SongBase(BaseModel):
    id: int
    title: str
    artist: str

class SongCreate(BaseModel):
    title: str
    artist: str

class Song(SongBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class SongUpdate(BaseModel):
    title: str
    artist: str
    
# User Stuff

class UserBase(BaseModel):
    id: int
    username: str
    show_no: Union[int, None] = None
    is_Admin: Union[bool, None] = None

class UserCreate(BaseModel):
    username: str
    show_no: int

class AdminCreate(BaseModel):
    username: str
    password: str
    is_Admin: bool

class User(UserBase):
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True


# Login stuff

class UserCredentials(BaseModel):
    username: str
    password: str


# Token Response

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    exp: int
    sub: Union[str, int]


class Healthz(BaseModel):
    status: str