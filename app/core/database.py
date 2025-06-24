"""Database configuration and session management"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables"""
    from app.models.database import Product, User, CartItem
    Base.metadata.create_all(bind=engine)
    
    # Create default admin user
    db = SessionLocal()
    try:
        from app.services.user_service import UserService
        user_service = UserService(db)
        if not user_service.get_user_by_username("admin"):
            user_service.create_user(
                username="admin",
                email="admin@rolex-store.com",
                password="admin123",
                is_admin=True
            )
    finally:
        db.close()