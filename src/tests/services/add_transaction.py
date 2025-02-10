from app.services.add_transaction import AddTransaction
from datetime import datetime
from app.schemas.transaction import (
    TransactionDataRequest,
    TransactionResponseSuccess,
    TransactionResponseFailed,
    TransactionErrorCode,
    TransactionMessage,
)


user_id = "1"
payer_id="1"
points=-10000
timestamp = datetime.now()


request = TransactionDataRequest(user_id=user_id, payer_id=payer_id, points=points, timestamp=timestamp)
AddTransaction.add_transaction(request)