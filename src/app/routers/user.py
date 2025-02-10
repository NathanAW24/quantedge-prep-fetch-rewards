from typing import Union
from fastapi import APIRouter
from app.schemas.spend_points import (
    SpendPointsDataRequest,
    SpendPointsResponseSuccess,
    SpendPointsResponseFailed
)
from app.services.spend_points import SpendPoints


router = APIRouter()

@router.post("/spend_points", response_model=Union[SpendPointsResponseSuccess, SpendPointsResponseFailed])
def get_transactions(request: SpendPointsDataRequest):
    return SpendPoints.spend_points(request)
