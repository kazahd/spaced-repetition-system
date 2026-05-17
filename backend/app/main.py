from fastapi import FastAPI

from app.db.database import engine, Base

from app.models import *


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spaced Repetition System API"
)


@app.get("/")
def root():
    return {"message": "API is working"}