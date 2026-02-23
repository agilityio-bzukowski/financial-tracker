import uuid
from datetime import datetime, timezone

from fastapi import HTTPException

from app.db.schema import Account
from app.models.account import AccountCreate, AccountUpdate
from app.services.base import BaseService


class AccountsService(BaseService):
    def list_accounts(self) -> list[Account]:
        return (
            self.session.query(Account)
            .filter(Account.deleted_at.is_(None))
            .order_by(Account.sort_order)
            .all()
        )

    def get_account(self, account_id: uuid.UUID) -> Account:
        account = (
            self.session.query(Account)
            .filter(Account.id == account_id, Account.deleted_at.is_(None))
            .first()
        )
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        return account

    def create_account(self, body: AccountCreate) -> Account:
        account = Account(**body.model_dump())
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def update_account(self, account_id: uuid.UUID, body: AccountUpdate) -> Account:
        account = self.get_account(account_id)
        updates = body.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(account, field, value)
        self.session.commit()
        self.session.refresh(account)
        return account

    def delete_account(self, account_id: uuid.UUID) -> None:
        account = self.get_account(account_id)
        account.deleted_at = datetime.now(timezone.utc)
        self.session.commit()
