from pydantic import BaseModel


class DeckCreate(BaseModel):
    title: str
    description: str | None = None


class DeckResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    owner_id: int

    class Config:
        from_attributes = True