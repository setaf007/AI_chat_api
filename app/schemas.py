from pydantic import BaseModel, EmailStr, Field
from typing import List
from datetime import datetime

from app.auth import Token

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=64)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True # Pydantic v2: ORM mode

class TokenResponse(Token):
    pass # from auth.py

class ChatCreate(BaseModel):
    title: str | None = None

class ChatBase(BaseModel):
    title: str  | None = None

class ChatOut(ChatBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ChatDetailOut(ChatOut):
    messages: List["MessageOut"] = []

    class Config:
        from_attributes = True

class MessageBase(BaseModel):
    role: str
    content: str

class MessageOut(MessageBase):
    id: int
    chat_id: int
    created_at: datetime

    class Config:
        from_attributes = True