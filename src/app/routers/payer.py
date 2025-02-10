from typing import Union
from fastapi import APIRouter
from app.schemas.points_balance import PointsBalanceResponseFailed, PointsBalanceResponseSuccess
from app.services.points_balance import PointsBalance


router = APIRouter()

@router.get("/points_balance", response_model=Union[PointsBalanceResponseSuccess, PointsBalanceResponseFailed])
def get_points_balance():
    return PointsBalance.points_balance()
