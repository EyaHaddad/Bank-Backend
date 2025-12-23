"""OTP module for one-time password management."""

#from .router import router
from .service import OTPService, OTPMessages
from .schemas import (
    OTPGenerateRequest,
    OTPVerifyRequest,
    OTPResponse,
    OTPVerifyResponse,
    OTPGenerateResponse,
)

__all__ = [
    "router",
    "OTPService",
    "OTPMessages",
    "OTPGenerateRequest",
    "OTPVerifyRequest",
    "OTPResponse",
    "OTPVerifyResponse",
    "OTPGenerateResponse",
]
