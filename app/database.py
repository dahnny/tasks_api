"""
Database configuration and connection setup.

This module handles the SQLAlchemy database engine configuration,
session management, and provides a dependency for database connections
in FastAPI endpoints.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL
from app.config import settings

# Construct PostgreSQL database URL from configuration settings
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg2",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_hostname,
    port=settings.database_port,
    database=settings.database_name
)

# Create SQLAlchemy engine with connection pooling and logging
engine = create_engine(DATABASE_URL, echo=True)

# Create SessionLocal class for database session management
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Database dependency for FastAPI endpoints.
    
    This function provides a database session that is automatically closed
    after the request is completed. It's designed to be used as a FastAPI
    dependency to inject database sessions into route handlers.
    
    Yields:
        Session: SQLAlchemy database session
        
    Note:
        The session is automatically closed in the finally block to ensure
        proper resource cleanup even if an exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
