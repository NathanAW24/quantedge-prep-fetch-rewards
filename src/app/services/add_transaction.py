from datetime import datetime
from typing import Self
from app.crud.payer import (
    get_payer_by_id,
    update_payer
)
from app.crud.user import (
    get_user_by_id,
    update_user
)
from app.crud.transaction import (
    create_transaction
)
from app.schemas.transaction import (
    TransactionDataRequest,
    TransactionResponseSuccess,
    TransactionResponseFailed,
    TransactionErrorCode,
    TransactionMessage,
)

class AddTransaction:
    @staticmethod
    def add_transaction(request: TransactionDataRequest):

        # get payer and user
        payer = get_payer_by_id(request.payer_id)
        user = get_user_by_id(request.user_id)

        # print(payer.points, "\n" ,user.points)
        if request.points > 0: # points > 0 --> user adds points, payer reduce points
            if request.points > payer.points:
                return TransactionResponseFailed(
                    success=False,
                    message=TransactionMessage.MSG_FAILED_PAYER_NOT_ENOUGH,
                    error_code=TransactionErrorCode.ERR_FAILED_PAYER_NOT_ENOUGH
                )
            else: # enough money
                # business logic
                # print(user.id, user)
                # print(payer.id, payer)

                user.points += request.points
                payer.points -= request.points

                # update in db
                update_user(user_id=user.id, update_data = { "points" : user.points })
                update_payer(payer_id=payer.id, update_data = { "points" : payer.points })

                create_transaction(
                    transaction_data = {
                        "user_id": user.id,
                        "payer_id": payer.id,
                        "points": request.points,
                        "timestamp": request.timestamp
                    }
                )

                # print(user)
                # print(payer)
                return TransactionResponseSuccess(
                    success=True,
                    message=TransactionMessage.MSG_SUCCESS_ADD_TO_USER,
                    data=request
                )
        else: # request.points <= 0 --> user reduce points, payer adds points
            if request.points > user.points:
                return TransactionResponseFailed(
                    success=False,
                    message=TransactionMessage.MSG_FAILED_USER_NOT_ENOUGH,
                    error_code=TransactionErrorCode.ERR_FAILED_USER_NOT_ENOUGH
                )
            else: # enough money
                user.points += request.points # this is a negative number
                payer.points -= request.points

                update_user(user_id=user.id, update_data = { "points" : user.points })
                update_payer(payer_id=payer.id, update_data = { "points" : payer.points })

                create_transaction(
                    transaction_data = {
                        "user_id": user.id,
                        "payer_id": payer.id,
                        "points": request.points,
                        "timestamp": request.timestamp
                    }
                )


                # print(user)
                # print(payer)

                return TransactionResponseSuccess(
                    success=True,
                    message=TransactionMessage.MSG_SUCCESS_DEDUCT_FROM_USER,
                    data=request
                )
