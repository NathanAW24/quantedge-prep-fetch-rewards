from pydantic import BaseModel

class Payer(BaseModel):
    id: str
    name: str
    points: int
