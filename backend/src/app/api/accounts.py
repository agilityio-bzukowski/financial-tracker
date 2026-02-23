import uuid

from fastapi import APIRouter, Depends

from app.db.session import SessionLocal
from app.models.account import AccountCreate, AccountResponse, AccountUpdate
from app.services.accounts import AccountsService

router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_accounts_service() -> AccountsService:
    return AccountsService(session=SessionLocal())


AccountsServiceDep = Depends(get_accounts_service)


@router.get("/", response_model=list[AccountResponse])
def list_accounts(service: AccountsService = AccountsServiceDep):
    return service.list_accounts()


@router.post("/", response_model=AccountResponse, status_code=201)
def create_account(body: AccountCreate, service: AccountsService = AccountsServiceDep):
    return service.create_account(body)


@router.get("/{account_id}", response_model=AccountResponse)
def get_account(account_id: uuid.UUID, service: AccountsService = AccountsServiceDep):
    return service.get_account(account_id)


@router.patch("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: uuid.UUID,
    body: AccountUpdate,
    service: AccountsService = AccountsServiceDep,
):
    return service.update_account(account_id, body)


@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: uuid.UUID, service: AccountsService = AccountsServiceDep):
    service.delete_account(account_id)
