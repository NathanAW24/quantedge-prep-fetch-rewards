from fastapi import FastAPI
from app.routers.transaction import router as transactions_router
from app.routers.user import router as users_router
from app.routers.payer import router as payers_router
from app.dependencies import run_init

run_init()
app = FastAPI(title="Fetch Rewards Exercise")
app.include_router(transactions_router, prefix="/transactions")
app.include_router(users_router, prefix = "/users")
app.include_router(payers_router, prefix = "/payers")