"""Route registration module."""

from fastapi import FastAPI
from src.modules.accounts.router import router as accounts_router
from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as users_router
from src.modules.transactions.router import router as transactions_router
from src.modules.otps.router import router as otps_router


def register_routes(app: FastAPI):
    """Register all API routes with /api prefix."""
    app.include_router(accounts_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    app.include_router(users_router, prefix="/api")
    app.include_router(transactions_router, prefix="/api")
    app.include_router(otps_router, prefix="/api")
