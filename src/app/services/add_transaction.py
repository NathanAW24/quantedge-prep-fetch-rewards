from datetime import datetime

class AddTransaction:
    def add_transaction(self, user_id: str, payer_id: str, points: int, timestamp: datetime):
        # 1. points > 0 --> user adds points, payer reduce points

        # get payer
        return