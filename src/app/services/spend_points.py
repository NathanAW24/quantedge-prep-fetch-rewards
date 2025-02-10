
from datetime import datetime

import pytz
from app.schemas.spend_points import (
    SpendPointsDataRequest,
    SpendPointsResponseSuccess,
    SpendPointsResponseFailed,
    SpendPointsMessage,
    SpendPointsErrorCode,
    SpendPointsDataResponse
)
from app.crud.user import get_user_by_id
from app.crud.transaction import get_all_transactions_with_user_id, update_transaction_expiry, update_transaction_points
from app.services.add_transaction import AddTransaction

from app.models.transaction import Transaction
from app.schemas.transaction import (
    TransactionDataRequest
)
from app.crud.payer import get_payer_by_id


class SpendPoints:
    @staticmethod
    def spend_points(request: SpendPointsDataRequest):
        # get user by id
        user = get_user_by_id(request.user_id)
        # print("USER",user) # OK

        # not enough points
        if request.points > user.points:
            return SpendPointsResponseFailed(
                success=False,
                message=SpendPointsMessage.MSG_FAILED_NOT_ENOUGH_USER_POINTS,
                error_code=SpendPointsErrorCode.ERR_FAILED_NOT_ENOUGH_USER_POINTS
            )

        else: # enough points

            # get all transactions that has user_id of request.user_id
            transactions = get_all_transactions_with_user_id(user.id) # sorted ascending

            new_transactions_log = SpendPoints.__deduct_points(transactions, request.points)

            return SpendPointsResponseSuccess(
                success=True,
                message=SpendPointsMessage.MSG_SUCCESS_POINTS_SPEND,
                data=new_transactions_log
            )
    
    @staticmethod
    def __deduct_points(transactions, points_to_deduct):

        new_transactions_log = []
        
        for transaction in transactions:
            # get payer
            payer = get_payer_by_id(transaction.payer_id)
            if transaction.points <= points_to_deduct:
                AddTransaction.add_transaction(TransactionDataRequest(user_id=transaction.user_id, payer_id=transaction.payer_id, points=-1*transaction.points, timestamp=datetime.utcnow().replace(tzinfo=pytz.UTC)))
                update_transaction_expiry(transaction_id=transaction.id)
                new_transactions_log.append(
                    SpendPointsDataResponse(
                        payer= payer.name,
                        points= -1*transaction.points
                    )
                )
                points_to_deduct -= transaction.points
            else: # transaction.points > points_to_deduct
                AddTransaction.add_transaction(TransactionDataRequest(user_id=transaction.user_id, payer_id=transaction.payer_id, points=-1*points_to_deduct, timestamp=datetime.utcnow().replace(tzinfo=pytz.UTC)))
                update_transaction_expiry(transaction_id=transaction.id)

                AddTransaction.add_transaction(TransactionDataRequest(user_id=transaction.user_id, payer_id=transaction.payer_id, points=transaction.points-points_to_deduct, timestamp=transaction.timestamp))

                new_transactions_log.append(
                    SpendPointsDataResponse(
                        payer= payer.name,
                        points= -1*points_to_deduct
                    )
                )
                points_to_deduct -= points_to_deduct
                return new_transactions_log
        
        return new_transactions_log
