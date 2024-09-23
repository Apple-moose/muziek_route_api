
from typing import Union, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Song stuff

class SongBase(BaseModel):
    id: int
    title: str
    artist: str

class SongCreate(BaseModel):
    title: str
    artist: int

class Song(SongBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

class SongUpdate(BaseModel):
    title: str
    artist: int




# User Stuff

class UserBase(BaseModel):
    id: int
    username: str
    imageUrl: Union[str, None] = None
    is_Admin: Union[bool, None] = None

class UserCreate(BaseModel):
    username: str


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