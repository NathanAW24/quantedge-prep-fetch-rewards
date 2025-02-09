from fastapi import FastAPI
from app.routers.transaction_router import router as transactions_router
from .dependencies import run_migration

run_migration()
app = FastAPI(title="Fetch Rewards Exercise")
app.include_router(transactions_router, prefix="/transactions")