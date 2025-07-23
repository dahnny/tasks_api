"""
Configuration settings for the Task Management API.

This module contains the application configuration using Pydantic Settings
to handle environment variables and application settings.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    This class defines all the configuration parameters needed for the application
    including database connection details, JWT settings, and other environment-specific
    configurations.
    
    Attributes:
        database_hostname (str): Database server hostname
        database_port (str): Database server port
        database_username (str): Database username
        database_password (str): Database password
        database_name (str): Database name
        secret_key (str): Secret key for JWT token generation
        algorithm (str): Algorithm used for JWT token encoding
        access_token_expire_minutes (str): Token expiration time in minutes
    """
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: str
    
    class Config:
        """Configuration for pydantic settings to load from .env file."""
        env_file = ".env"

# Global settings instance
settings = Settings()