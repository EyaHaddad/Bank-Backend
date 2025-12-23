"""Admin module package."""

from .router import router
from .service import promote_user_to_admin

__all__ = [
    "router",
    "promote_user_to_admin",
]
