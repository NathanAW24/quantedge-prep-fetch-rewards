from enum import Enum
from pydantic import BaseModel

class PointsBalanceResponseMessage(str, Enum):
    MSG_POINTS_BALANCE_SUCCESS = "points balance retrieved for all payers"
    MSG_POINTS_BALANCE_FAILED = "no payers found"

class PointsBalanceResponseErrorCode(str, Enum):
    ERR_CODE_POINTS_BALANCE_FAILED = "NO_PAYERS_FOUND"

class PointsBalanceResponseBase(BaseModel):
    success: bool
    message: str

class PointsBalanceResponseSuccess(PointsBalanceResponseBase):
    data: dict[str, int]

class PointsBalanceResponseFailed(PointsBalanceResponseBase):
    error_code: str
