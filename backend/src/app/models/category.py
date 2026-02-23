import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.db.schema import TransactionType


class CategoryCreate(BaseModel):
    name: str
    type: TransactionType
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: float = 0.0

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("name must not be empty")
        return v.strip()


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[TransactionType] = None
    color: Optional[str] = None
    icon: Optional[str] = None
    sort_order: Optional[float] = None

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError("name must not be empty")
        return v.strip() if v else v


class CategoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    type: TransactionType
    color: Optional[str]
    icon: Optional[str]
    sort_order: float
    created_at: datetime
    updated_at: datetime
