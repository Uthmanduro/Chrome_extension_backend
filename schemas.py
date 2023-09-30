from pydantic import BaseModel, Field


class Video(BaseModel):
    url: str = Field(..., example="video url")

    class Config:
        orm_mode = True
