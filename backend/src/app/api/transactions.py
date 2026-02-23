import uuid

from fastapi import APIRouter, Depends

from app.db.session import SessionLocal
from app.models.transaction import TransactionCreate, TransactionResponse, TransactionUpdate
from app.services.transactions import TransactionsService

router = APIRouter(prefix="/transactions", tags=["transactions"])


def get_transactions_service() -> TransactionsService:
    return TransactionsService(session=SessionLocal())


TransactionsServiceDep = Depends(get_transactions_service)


@router.get("/", response_model=list[TransactionResponse])
def list_transactions(service: TransactionsService = TransactionsServiceDep):
    return service.list_transactions()


@router.post("/", response_model=TransactionResponse, status_code=201)
def create_transaction(
    body: TransactionCreate, service: TransactionsService = TransactionsServiceDep
):
    return service.create_transaction(body)


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: uuid.UUID, service: TransactionsService = TransactionsServiceDep
):
    return service.get_transaction(transaction_id)


@router.patch("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: uuid.UUID,
    body: TransactionUpdate,
    service: TransactionsService = TransactionsServiceDep,
):
    return service.update_transaction(transaction_id, body)


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction(
    transaction_id: uuid.UUID, service: TransactionsService = TransactionsServiceDep
):
    service.delete_transaction(transaction_id)
