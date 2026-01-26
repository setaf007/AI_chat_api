from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Depends

from app.core.config import settings
from app.routers import users

from sqlalchemy.orm import Session
from app.dependencies import get_db

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # during dev, restrict in prod
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(users.router)
    # app.include_router(chats.router, prefix="/chats", tags=["chats"])

    @app.get("/health", tags=["health"])
    async def health_check(db: Session = Depends(get_db)):
        users_table_exists = db.bind.dialect.has_table(db.bind.connect(), "users")
        
        return {
            "status": "ok",
            "env": settings.app_env,
            "lmstudio_base_url": str(settings.lmstudio_base_url),
            "db_users_table": users_table_exists,
            }
    
    return app

app = create_app()