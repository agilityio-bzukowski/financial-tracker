import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.db.schema import TransactionType
from app.models.account import AccountResponse
from app.models.category import CategoryResponse


class TransactionCreate(BaseModel):
    account_id: uuid.UUID
    category_id: Optional[uuid.UUID] = None
    type: TransactionType
    amount: float
    description: Optional[str] = None
    date: datetime
    is_reconciled: bool = False
    sort_order: float = 0.0

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("amount must be greater than zero")
        return v


class TransactionUpdate(BaseModel):
    account_id: Optional[uuid.UUID] = None
    category_id: Optional[uuid.UUID] = None
    type: Optional[TransactionType] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    date: Optional[datetime] = None
    is_reconciled: Optional[bool] = None
    sort_order: Optional[float] = None

    @field_validator("amount")
    @classmethod
    def amount_positive(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and v <= 0:
            raise ValueError("amount must be greater than zero")
        return v


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    account_id: uuid.UUID
    category_id: Optional[uuid.UUID]
    type: TransactionType
    amount: float
    description: Optional[str]
    date: datetime
    is_reconciled: bool
    sort_order: float
    created_at: datetime
    updated_at: datetime
    account: AccountResponse
    category: Optional[CategoryResponse]
