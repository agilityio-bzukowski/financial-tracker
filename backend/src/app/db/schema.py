import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_now, onupdate=_now, nullable=False
    )


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class AccountType(str, enum.Enum):
    checking = "checking"
    savings = "savings"
    credit_card = "credit_card"
    cash = "cash"
    other = "other"


class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"


class AIProvider(str, enum.Enum):
    anthropic = "anthropic"
    openai = "openai"
    ollama = "ollama"


# ---------------------------------------------------------------------------
# Settings  (singleton — id is always "default")
# ---------------------------------------------------------------------------


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[str] = mapped_column(String, primary_key=True, default="default")  # type: ignore[assignment]
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    ai_provider: Mapped[AIProvider] = mapped_column(
        SAEnum(AIProvider, name="aiprovider"), nullable=False, default=AIProvider.anthropic
    )
    ai_model: Mapped[str] = mapped_column(
        String(128), nullable=False, default="claude-sonnet-4-6"
    )


# ---------------------------------------------------------------------------
# Account
# ---------------------------------------------------------------------------


class Account(Base):
    __tablename__ = "accounts"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    type: Mapped[AccountType] = mapped_column(
        SAEnum(AccountType, name="accounttype"), nullable=False
    )
    balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="USD")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    sort_order: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="account"
    )


# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(128), nullable=False)
    type: Mapped[TransactionType] = mapped_column(
        SAEnum(TransactionType, name="transactiontype"), nullable=False
    )
    color: Mapped[Optional[str]] = mapped_column(String(7), nullable=True)
    icon: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    sort_order: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    transactions: Mapped[list["Transaction"]] = relationship(
        "Transaction", back_populates="category"
    )


# ---------------------------------------------------------------------------
# Transaction
# ---------------------------------------------------------------------------


class Transaction(Base):
    __tablename__ = "transactions"

    account_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("accounts.id"), nullable=False
    )
    category_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )
    type: Mapped[TransactionType] = mapped_column(
        SAEnum(TransactionType, name="transactiontype"),
        nullable=False,
    )
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    is_reconciled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    account: Mapped["Account"] = relationship("Account", back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship(
        "Category", back_populates="transactions"
    )
