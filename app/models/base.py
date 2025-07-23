"""
SQLAlchemy base model for all database models.

This module provides the declarative base class that all database models
in the application inherit from.
"""

from sqlalchemy.ext.declarative import declarative_base

# Base class for all SQLAlchemy models
Base = declarative_base()