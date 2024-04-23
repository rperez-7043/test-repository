from datetime import datetime
from pydantic import BaseModel, EmailStr


class JokeBase(BaseModel):
    setup: str
    punchline: str
    published: bool = True


class JokeCreate(JokeBase):
    pass


class JokeUpdate(BaseModel):
    setup: str
    punchline: str


class JokeResponse(JokeBase):
    id: int
    create_date: datetime


class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int | None = None
