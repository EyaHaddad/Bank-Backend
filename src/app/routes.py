"""Route registration module."""

from fastapi import FastAPI
from src.modules.accounts.router import router as accounts_router
from src.modules.auth.router import router as auth_router
from src.modules.users.router import router as users_router
from src.modules.transactions.router import router as transactions_router
from src.modules.transfers.router import router as transfers_router
from src.modules.beneficiaries.router import router as beneficiaries_router
from src.modules.otps.router import router as otps_router
from src.modules.notifications.router import router as notifications_router
from src.modules.admin.router import router as admin_router
from src.modules.currency.router import router as currency_router


def register_routes(app: FastAPI):
    """Register all API routes with /api prefix."""
    app.include_router(accounts_router, prefix="/api")
    app.include_router(auth_router, prefix="/api")
    app.include_router(users_router, prefix="/api")
    app.include_router(transactions_router, prefix="/api")
    app.include_router(transfers_router, prefix="/api")
    app.include_router(beneficiaries_router, prefix="/api")
    app.include_router(otps_router, prefix="/api")
    app.include_router(notifications_router, prefix="/api")
    app.include_router(admin_router, prefix="/api")
    app.include_router(currency_router, prefix="/api")
