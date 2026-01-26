from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app import models, schemas
from app.auth import get_password_hash, verify_password

from typing import List

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user with hashed password."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> models.User | None:
    """Authenticate user by email and password."""
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_chat(db: Session, title: str | None, user_id: int) -> models.Chat:
    """Create a new chat for a user."""
    db_chat = models.Chat(title=title, user_id=user_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

def get_user_chats(db: Session, user_id: int) -> List[models.Chat]:
    """Retrieve all chats for a given user."""
    return db.query(models.Chat).filter(models.Chat.user_id == user_id).order_by(
        models.Chat.created_at.desc()
    ).all()

def create_message(db: Session, role: str, content: str, chat_id: int) -> models.Message:
    """Create a new message in a chat."""
    db_message = models.Message(chat_id=chat_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_chat_messages(db: Session, chat_id: int, limit: int=20) -> List[models.Message]:
    """Retrieve messages for a given chat, limited by the specified number."""
    return (
        db.query(models.Message)
        .filter(models.Message.chat_id == chat_id)
        .order_by(models.Message.created_at.asc())
        .limit(limit)
        .all()
    )