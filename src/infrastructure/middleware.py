"""
Middleware module for the FastAPI backend.

This module centralizes all middleware configuration and custom middleware classes
for the banking application. It provides security, performance monitoring, and
request handling capabilities.

Middleware Stack (applied in reverse order):
    1. AdvancedSecurityMiddleware - Rate limiting, timing, security headers, logging
    2. GZipMiddleware - Response compression for large payloads
    3. TrustedHostMiddleware - Host header validation
    4. CORSMiddleware - Cross-Origin Resource Sharing configuration
"""

import time
import logging
from collections import defaultdict
from typing import Dict, List, Set

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from src.config import settings

logger = logging.getLogger(__name__)

class AdvancedSecurityMiddleware(BaseHTTPMiddleware):
    """
    Advanced HTTP middleware combining multiple security and monitoring features.

    Attributes:
        rate_limit_records (Dict[str, float]): Tracks last request time per client IP.
        rate_limit_seconds (float): Minimum time interval between requests per IP.
    """
    EXCLUDED_PATHS: Set[str] = {
        "/docs",
        "/redoc",
        "/favicon.ico",
        "/openapi.json",
        "/api/openapi.json",
    }

    def __init__(self, app: FastAPI, rate_limit_seconds: float = 1.0) -> None:
        """
        Initialize the AdvancedSecurityMiddleware.

        Args:
            app: The FastAPI application instance.
            rate_limit_seconds: Minimum seconds between requests from same IP.
                               Defaults to 1.0 second.
        """
        super().__init__(app)
        self.rate_limit_records: Dict[str, float] = defaultdict(float)
        self.rate_limit_seconds = rate_limit_seconds

    async def log_message(self, message: str) -> None:
        """
        Log a message asynchronously.

        Args:
            message: The message to log.
        """
        logger.info(message)

    async def dispatch(self, request: Request, call_next):
        """
        Process the incoming request through the middleware pipeline.

        This method handles:
            1. Rate limiting check based on client IP
            2. Request logging
            3. Request processing and timing
            4. Security headers injection
            5. Response logging

        Args:
            request: The incoming HTTP request.
            call_next: The next middleware or route handler in the chain.

        Returns:
            Response: The HTTP response with added security headers.

        Raises:
            HTTP 429: If rate limit is exceeded for the client IP.
        """
        path = request.url.path

        # Skip rate limiting for public/static endpoints
        if settings.DEBUG and path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Extract client information
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()

        # Rate Limiting Check
        # Prevents abuse by limiting request frequency per client IP
        if current_time - self.rate_limit_records[client_ip] < self.rate_limit_seconds:
            await self.log_message(f"Rate limit exceeded for {client_ip} on {path}")
            return Response(content="Rate limit exceeded", status_code=429)

        self.rate_limit_records[client_ip] = current_time

        # Log incoming request
        await self.log_message(f"Request to {path} from {client_ip}")

        # Process Request & Measure Time
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Add process time header for performance monitoring
        response.headers["X-Process-Time"] = str(process_time)

        # Security Headers Injection
        # Adds standard security headers to protect against common attacks
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking by disabling iframe embedding
        response.headers["X-Frame-Options"] = "DENY"
        
        # Enable XSS filter in browsers
        response.headers["X-XSS-Protection"] = "1; mode=block"

        # Content Security Policy - relaxed in debug mode for Swagger UI
        if settings.DEBUG:
            response.headers["Content-Security-Policy"] = (
                "default-src 'self' https://cdn.jsdelivr.net; "
                "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
                "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
                "img-src 'self' data: https://cdn.jsdelivr.net;"
            )
        else:
            # Strict CSP for production
            response.headers["Content-Security-Policy"] = "default-src 'self'"

        # Log response time for monitoring
        await self.log_message(f"Response for {path} took {process_time:.4f} seconds")

        return response

# MIDDLEWARE REGISTRATION

def setup_middleware(app: FastAPI) -> None:
    """
    Configure and register all middleware for the FastAPI application.

    This function sets up the complete middleware stack in the correct order.
    Middleware is applied in reverse order of registration, so the last
    middleware added is the first to process requests.

    Middleware Stack Order (request flow):
        1. CORSMiddleware - Handles CORS preflight and headers
        2. TrustedHostMiddleware - Validates Host header
        3. GZipMiddleware - Compresses large responses
        4. AdvancedSecurityMiddleware - Security headers, rate limiting, logging

    Args:
        app: The FastAPI application instance to configure.
    """
        # CORS Middleware
    # Handles Cross-Origin Resource Sharing for frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,  # Allowed frontend origins
        allow_credentials=True,                   # Allow cookies/auth headers
        allow_methods=["GET", "POST", "PUT", "DELETE"],  # Allowed HTTP methods
        allow_headers=["*"],                     # Allow all headers
        max_age=3600,                            # Cache preflight for 1 hour
    )

    # Trusted Host Middleware
    # Protects against HTTP Host header attacks
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS,    # Valid host headers
    )

    # GZip Compression Middleware
    # Compresses responses larger than minimum_size bytes
    app.add_middleware(
        GZipMiddleware,
        minimum_size=1000,                       # Compress responses > 1KB
    )

    # Advanced Security Middleware (Custom)
    # Rate limiting, process timing, security headers, async logging
    app.add_middleware(
        AdvancedSecurityMiddleware,
        rate_limit_seconds=1.0,                  # 1 request per second per IP
    )
