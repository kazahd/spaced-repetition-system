from pydantic import BaseModel


class ReviewRequest(BaseModel):
    quality: int