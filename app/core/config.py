"""Application configuration settings"""

import os
from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Application
    APP_NAME: str = "Rolex Luxury Timepieces"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Security
    SECRET_KEY: str = "luxury-swiss-timepieces-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "sqlite:///./rolex_store.db"
    
    # Static files
    STATIC_URL: str = "/static"
    MEDIA_URL: str = "/media"
    
    # External APIs
    UNSPLASH_ACCESS_KEY: str = ""  # Optional for better images
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()