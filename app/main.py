from fastapi import FastAPI
from app.models.base import Base
from app.database import engine
from app.models.user import User

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

Base.metadata.create_all(bind=engine)

