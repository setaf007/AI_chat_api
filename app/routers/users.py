from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, schemas
from app.dependencies import get_db
from app.auth import create_access_token

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    return db_user

@router.post("/login", response_model=schemas.TokenResponse)
def login(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create JWT token
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}