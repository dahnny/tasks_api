# Task Management API

A comprehensive RESTful API for task management with user authentication, built with FastAPI, SQLAlchemy, and PostgreSQL.

## 🚀 Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Task Management**: Full CRUD operations for tasks with user ownership
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **API Documentation**: Automatic OpenAPI/Swagger documentation
- **Security**: Bcrypt password hashing and JWT token-based authorization
- **Testing**: Comprehensive test suite with pytest
- **Data Validation**: Pydantic schemas for request/response validation

## 📋 Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
- pip (Python package manager)

### Clone the Repository

```bash
git clone <repository-url>
cd api_tasks
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Database Configuration
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=your_db_username
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=taskmanagement

# JWT Configuration
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Environment Variables Explanation

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_HOSTNAME` | PostgreSQL server hostname | `localhost` |
| `DATABASE_PORT` | PostgreSQL server port | `5432` |
| `DATABASE_USERNAME` | Database username | `postgres` |
| `DATABASE_PASSWORD` | Database password | `password123` |
| `DATABASE_NAME` | Database name | `taskmanagement` |
| `SECRET_KEY` | JWT secret key for token signing | `your-secret-key` |
| `ALGORITHM` | JWT encoding algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |

## 🗄️ Database Setup

### Create Database

```sql
-- Connect to PostgreSQL and create database
CREATE DATABASE taskmanagement;
```

### Database Schema

The application automatically creates the following tables:

#### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

#### Tasks Table
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    owner_id INTEGER REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    title VARCHAR NOT NULL,
    description VARCHAR,
    status VARCHAR DEFAULT 'INCOMPLETE' NOT NULL,
    due_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL
);
```

## 🚀 Running the Application

### Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🔗 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/auth/login` | User login and token generation | No |

### User Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/users/` | Register a new user | No |
| GET | `/users/{user_id}` | Get user profile by ID | No |

### Task Endpoints

| Method | Endpoint | Description | Authentication |
|--------|----------|-------------|----------------|
| POST | `/tasks/` | Create a new task | Required |
| GET | `/tasks/` | Get paginated list of user's tasks | Required |
| GET | `/tasks/{task_id}` | Get specific task by ID | Required |
| PUT | `/tasks/{task_id}` | Update an existing task | Required |
| DELETE | `/tasks/{task_id}` | Delete a task | Required |

### Example API Calls

#### Register a New User
```bash
curl -X POST "http://localhost:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

#### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=securepassword123"
```

#### Create a Task
```bash
curl -X POST "http://localhost:8000/tasks/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive API documentation",
    "status": "INCOMPLETE",
    "due_date": "2024-12-31T23:59:59"
  }'
```

#### Get Tasks with Pagination
```bash
curl -X GET "http://localhost:8000/tasks/?limit=10&skip=0" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register**: Create a new user account using `/users/` endpoint
2. **Login**: Authenticate using `/auth/login` to receive a JWT token
3. **Authorization**: Include the token in the `Authorization` header as `Bearer {token}`
4. **Token Expiration**: Tokens expire after 30 minutes (configurable)

### Security Features

- **Password Hashing**: Bcrypt with automatic salt generation
- **JWT Tokens**: Secure token-based authentication
- **User Isolation**: Users can only access their own tasks
- **Input Validation**: Pydantic schemas validate all inputs

## 🧪 Testing

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test Files

```bash
pytest tests/test_task.py
```

### Test Database

Tests use a separate database (`{DATABASE_NAME}_test`) to ensure isolation from production data.

## 📁 Project Structure

```
api_tasks/
│
├── app/                          # Main application package
│   ├── __init__.py              # Package initialization with module docs
│   ├── main.py                  # FastAPI app setup and configuration
│   ├── config.py                # Environment configuration management
│   ├── database.py              # Database connection and session handling
│   ├── oauth2.py                # JWT authentication and authorization
│   ├── utils.py                 # Utility functions (password hashing)
│   │
│   ├── models/                  # SQLAlchemy database models
│   │   ├── __init__.py         # Models package documentation
│   │   ├── base.py             # Base model class
│   │   ├── user.py             # User model
│   │   └── task.py             # Task model
│   │
│   ├── schemas/                 # Pydantic validation schemas
│   │   ├── __init__.py         # Schemas package documentation
│   │   ├── user.py             # User data schemas
│   │   ├── task.py             # Task data schemas
│   │   └── token.py            # JWT token schemas
│   │
│   └── routes/                  # API endpoint definitions
│       ├── auth.py             # Authentication routes
│       ├── user.py             # User management routes
│       └── task.py             # Task management routes
│
├── tests/                       # Test suite
│   ├── conftest.py             # Pytest configuration and fixtures
│   └── test_task.py            # Task endpoint tests
│
├── .env                        # Environment variables (create this)
├── .gitignore                  # Git ignore rules
└── README.md                   # Project documentation
```

## 🛠️ Technologies Used

### Backend Framework
- **FastAPI**: Modern, fast web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications

### Database
- **PostgreSQL**: Advanced open-source relational database
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Psycopg2**: PostgreSQL adapter for Python

### Authentication & Security
- **Passlib**: Password hashing library with bcrypt
- **Python-Jose**: JWT token handling
- **Python-Multipart**: Form data parsing

### Data Validation
- **Pydantic**: Data validation using Python type annotations
- **Email-Validator**: Email format validation

### Testing
- **Pytest**: Testing framework
- **Pytest-Cov**: Coverage reporting

### Configuration
- **Pydantic-Settings**: Settings management with environment variables

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guidelines
- Add comprehensive docstrings to all functions and classes
- Write tests for new features
- Update documentation for API changes
- Ensure all tests pass before submitting PRs

## 📝 API Response Examples

### Successful Task Creation
```json
{
  "id": 1,
  "title": "Complete project documentation",
  "description": "Write comprehensive API documentation",
  "status": "INCOMPLETE",
  "due_date": "2024-12-31T23:59:59",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Response
```json
{
  "detail": "Task with id: 999 not found"
}
```

### Login Success Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Built with ❤️ using FastAPI and Python**