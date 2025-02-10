from datetime import datetime

# imports should be relative to the directory you are running the file from
from app.crud.transaction import create_transaction 

transaction_data = {
    'payer_id': '123',
    'user_id':'123',
    'timestamp': datetime.now(),
    'points': 2000
}

create_transaction(transaction_data)
