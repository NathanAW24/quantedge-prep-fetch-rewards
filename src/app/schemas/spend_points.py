from enum import Enum
from typing import List
from pydantic import BaseModel

class SpendPointsMessage(str, Enum):
    MSG_SUCCESS_POINTS_SPEND = "points succesfully spent by user"
    MSG_FAILED_NOT_ENOUGH_USER_POINTS = "user don't have enough points"

class SpendPointsErrorCode(str, Enum):
    ERR_FAILED_NOT_ENOUGH_USER_POINTS = "SPEND_POINTS_FAILED_NOT_ENOUGH"

class SpendPointsDataRequest(BaseModel):
    user_id: str
    points: int

class SpendPointsDataResponse(BaseModel):
    payer: str
    points: int

class SpendPointsResponseBase(BaseModel):
    success: bool
    message: SpendPointsMessage

class SpendPointsResponseSuccess(SpendPointsResponseBase):
    data: List[SpendPointsDataResponse]

class SpendPointsResponseFailed(SpendPointsResponseBase):
    error_code: SpendPointsErrorCode
