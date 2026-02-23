import uuid
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import joinedload

from app.db.schema import Transaction
from app.models.transaction import TransactionCreate, TransactionUpdate
from app.services.base import BaseService


class TransactionsService(BaseService):
    def _query(self):
        return (
            self.session.query(Transaction)
            .options(joinedload(Transaction.account), joinedload(Transaction.category))
            .filter(Transaction.deleted_at.is_(None))
        )

    def list_transactions(self) -> list[Transaction]:
        return self._query().order_by(Transaction.date.desc()).all()

    def get_transaction(self, transaction_id: uuid.UUID) -> Transaction:
        transaction = (
            self._query()
            .filter(Transaction.id == transaction_id)
            .first()
        )
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return transaction

    def create_transaction(self, body: TransactionCreate) -> Transaction:
        transaction = Transaction(**body.model_dump())
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return self.get_transaction(transaction.id)

    def update_transaction(
        self, transaction_id: uuid.UUID, body: TransactionUpdate
    ) -> Transaction:
        transaction = self.get_transaction(transaction_id)
        updates = body.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(transaction, field, value)
        self.session.commit()
        return self.get_transaction(transaction_id)

    def delete_transaction(self, transaction_id: uuid.UUID) -> None:
        transaction = self.get_transaction(transaction_id)
        transaction.deleted_at = datetime.now(timezone.utc)
        self.session.commit()
