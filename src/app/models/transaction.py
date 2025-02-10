
from pydantic import BaseModel
from datetime import datetime

class Transaction(BaseModel):
    id: str
    payer_id: str
    user_id: str

    timestamp: datetime
    points: int
