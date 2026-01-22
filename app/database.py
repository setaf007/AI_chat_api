from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Engine: low level connection to the DB
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if 
    settings.database_url.startswith("sqlite") else {},
    )

# Session factory: each request will get its own SessionLocal()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models
Base = declarative_base()