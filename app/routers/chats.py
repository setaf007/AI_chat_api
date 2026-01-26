from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List

from app import crud, schemas, models
from app.dependencies import get_db, get_current_user
from app.models import User
from app.lmstudio import chat_completion
from app.limiter import limiter

router = APIRouter(prefix="/chats", tags=["chats"])

@router.post("/", response_model=schemas.ChatOut)
async def create_chat(
    chat_create: schemas.ChatCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a new chat for the current user."""
    db_chat = crud.create_chat(db, chat_create.title, current_user.id)
    return db_chat

@router.get("/", response_model=List[schemas.ChatOut])
def list_chats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all chats for the current user."""
    chats = crud.get_user_chats(db, current_user.id)
    return chats

@router.get("/{chat_id}", response_model=schemas.ChatDetailOut)
async def get_chat(
    chat_id: int,
    include_messages: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get single chat + optional messages."""
    chat = db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.user_id == current_user.id,
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    if include_messages:
        chat_messages = crud.get_chat_messages(db, chat_id)

    return chat

@router.post("/{chat_id}/messages", response_model=schemas.MessageOut)
@limiter.limit("5/minute")
async def send_message(
    request: Request,
    chat_id: int,
    message: schemas.MessageBase,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Send user message → LM Studio → save both."""
    
    # Verify chat belongs to user
    chat = db.query(models.Chat).filter(
        models.Chat.id == chat_id,
        models.Chat.user_id == current_user.id,
    ).first()
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found",
        )
    
    # Save user message
    user_message = crud.create_message(
        db,
        "user",
        message.content,
        chat_id,
    )

    # Get recent context (last 10 messages)
    context = crud.get_chat_messages(db, chat_id, limit=10)
    messages = [{"role": m.role, "content": m.content} for m in context] + [{"role": "user", "content": message.content}]

    # Get LM Studio response
    try:
        ai_reply = await chat_completion(messages)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service unavailable: {str(e)}",
        )
    
    # Save AI message
    ai_message = crud.create_message(
        db,
        "assistant",
        ai_reply,
        chat_id,
    )

    return ai_message