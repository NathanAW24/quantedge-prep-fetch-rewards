from app.crud.payer import get_all_payers
from app.schemas.points_balance import PointsBalanceResponseFailed, PointsBalanceResponseMessage, PointsBalanceResponseErrorCode, PointsBalanceResponseSuccess


class PointsBalance:
    @staticmethod
    def points_balance():
        # get all payers
        # format payers to {name : points}
        payers = get_all_payers()
        # print('payer', payers)
        if not payers:
            return PointsBalanceResponseFailed(
                success=False,
                message=PointsBalanceResponseMessage.MSG_POINTS_BALANCE_FAILED,
                error_code=PointsBalanceResponseErrorCode.ERR_CODE_POINTS_BALANCE_FAILED
            )
        
        points_balance_dict = {}

        for payer in payers:
            points_balance_dict[payer.name] = payer.points

        print(points_balance_dict)

        return PointsBalanceResponseSuccess(
            success=True,
            message=PointsBalanceResponseMessage.MSG_POINTS_BALANCE_SUCCESS,
            data=points_balance_dict
        )




        
