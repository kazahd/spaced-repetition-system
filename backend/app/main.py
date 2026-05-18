from fastapi import FastAPI

from app.db.database import engine
from app.db.base_class import Base

# импорт моделей
from app.db.base import *

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.decks import router as decks_router



Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spaced Repetition System API"
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(decks_router)

@app.get("/")
def root():
    return {"message": "API is working"}