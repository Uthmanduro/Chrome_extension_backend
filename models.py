from sqlalchemy import Column, String, Integer
from db import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)