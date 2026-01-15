from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
# from app.routers import users, chats

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

    # Include routers later
    # app.include_router(users.router, prefix="/users", tags=["users"])
    # app.include_router(chats.router, prefix="/chats", tags=["chats"])

    @app.get("/health", tags=["health"])
    async def health_check():
        return {
            "status": "ok",
            "env": settings.app_env,
            "lmstudio_base_url": str(settings.lmstudio_base_url),
            }
    
    return app

app = create_app()