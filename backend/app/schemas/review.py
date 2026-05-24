from pydantic import BaseModel, Field


class ReviewRequest(BaseModel):
    quality: int = Field(
        ..., 
        ge=0, 
        le=5, 
        description="Качество ответа: 0 - забыл, 5 - идеальный ответ"
    )