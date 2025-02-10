from fastapi import FastAPI
from .routers.transaction import router as transactions_router
from .dependencies import run_migration

run_migration()
app = FastAPI(title="Fetch Rewards Exercise")
app.include_router(transactions_router, prefix="/transactions")
