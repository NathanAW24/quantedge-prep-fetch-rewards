from typing import Union
from fastapi import APIRouter
from app.schemas.transaction import (
    TransactionDataRequest,
    TransactionResponseSuccess,
    TransactionResponseFailed,
)

from app.services.add_transaction import AddTransaction


router = APIRouter()

@router.post("/", response_model=Union[TransactionResponseSuccess, TransactionResponseFailed])
def get_transactions(request: TransactionDataRequest):
    return AddTransaction.add_transaction(request)