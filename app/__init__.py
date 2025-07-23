"""
Task Management API Application Package

This package contains a FastAPI-based REST API for task management with user authentication.
The application provides endpoints for user registration, authentication, and CRUD operations
for task management with proper authorization.

Modules:
    - main: FastAPI application setup and configuration
    - config: Application configuration and settings management
    - database: Database connection and session management
    - oauth2: JWT authentication and authorization
    - utils: Utility functions for password hashing
    - models: SQLAlchemy database models
    - schemas: Pydantic data validation schemas
    - routes: API endpoint definitions and handlers
"""