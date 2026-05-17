from fastapi import FastAPI

from app.db.database import engine, Base

from app.models import *

from app.api.auth import router as auth_router

from app.api.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spaced Repetition System API"
)

app.include_router(auth_router)

app.include_router(users_router)

@app.get("/")
def root():
    return {"message": "API is working"}