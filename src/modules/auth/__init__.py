"""Auth module package."""

from .router import router
from .service import (
    authenticate_user,
    create_access_token,
    get_current_user,
    get_admin_user,
    require_admin,
    CurrentUser,
    AdminUser,
    register_user,
    login_user_access_token,
)

__all__ = [
    "router",
    "authenticate_user",
    "create_access_token",
    "get_current_user",
    "get_admin_user",
    "require_admin",
    "CurrentUser",
    "AdminUser",
    "register_user",
    "login_user_access_token",
]
