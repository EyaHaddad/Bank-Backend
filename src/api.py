from fastapi import FastAPI
from src.accounts.controller import router as accounts_router
from src.auth.controllers import router as auth_router
from src.users.controller import router as users_router
from src.transactions.controller import router as transactions_router

def register_routes(app: FastAPI):
    """Register all API routes with /api prefix."""
    app.include_router(accounts_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    app.include_router(users_router, prefix="/api")
    app.include_router(transactions_router, prefix="/api")