from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.orm import declarative_base

from app.enums import Categories

Base = declarative_base()



class FlipCard(Base):
    __tablename__ = "flipcards"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    front_text = Column(String, nullable=False, unique=True, index=True)
    back_text = Column(String)
    category = Column(Enum(Categories), nullable=False)
