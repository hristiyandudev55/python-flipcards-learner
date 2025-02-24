from typing import Optional

from pydantic import BaseModel


class BaseConfig(BaseModel):
    model_config = {"from_attributes": True}


class FlipCardCreate(BaseConfig):
    front_text: str
    back_text: str
    category: str


class CardQuestion(BaseModel):
    front_text: str


class CardAnswer(BaseModel):
    back_text: str


class CardEdit(BaseConfig):
    front_text: Optional[str] | None = None
    back_text: Optional[str] | None = None
    category: Optional[str] | None = None


class FlipCardResponse(BaseConfig):
    front_text: str
    back_text: str
    category: str
