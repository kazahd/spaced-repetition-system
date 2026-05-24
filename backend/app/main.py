from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine
from app.db.base_class import Base

# импорт моделей
from app.db.base import *
from app.middleware.audit import AuditMiddleware

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.decks import router as decks_router
from app.api.cards import router as cards_router
from app.api.reviews import router as reviews_router
from app.api.stats import router as stats_router
from app.api.admin import router as admin_router


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spaced Repetition System API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(decks_router)
app.include_router(cards_router)
app.include_router(reviews_router)
app.include_router(stats_router)
app.include_router(admin_router)

app.add_middleware(AuditMiddleware)

@app.get("/")
def root():
    return {"message": "API is working"}