from pydantic import BaseModel
from datetime import datetime
from typing import Literal, TypeAlias
from enum import Enum

class TransactionMessage(str, Enum):
    MSG_SUCCESS_ADD_TO_USER = "points added to user"
    MSG_SUCCESS_DEDUCT_FROM_USER = "points deducted from user"
    MSG_FAILED_USER_NOT_ENOUGH = "user don't have enough points to deduct"
    MSG_FAILED_PAYER_NOT_ENOUGH = "payer don't have enough points to give"

class TransactionErrorCode(str, Enum):
    ERR_FAILED_USER_NOT_ENOUGH = "TRANSACTION_FAILED_ADD_USER"
    ERR_FAILED_PAYER_NOT_ENOUGH = "TRANSACTION_FAILED_ADD_PAYER"


class TransactionDataRequest(BaseModel):
    user_id: str
    payer_id: str
    points: int
    timestamp: datetime

class TransactionResponseBase(BaseModel):
    success: bool
    message: TransactionMessage

class TransactionResponseSuccess(TransactionResponseBase):
    data: TransactionDataRequest

class TransactionResponseFailed(TransactionResponseBase):
    error_code: TransactionErrorCode
