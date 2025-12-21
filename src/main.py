"""
Main application file for the FastAPI backend.
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
import logging
from fastapi.security import OAuth2PasswordBearer
from src.app.routes import register_routes
from src.config import settings
from src.infrastructure.database import engine, Base
from src.infrastructure.middleware import setup_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
    openapi_url="/api/openapi.json" if settings.DEBUG else None,
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# Configure all middleware (CORS, TrustedHost, GZip, Security)
setup_middleware(app)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# Include routers
register_routes(app)

@app.get("/")
async def root():
    return {"message": "Secure Banking API", "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
@app.get("/ping")
def ping():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_keyfile=settings.SSL_KEY_FILE if settings.USE_SSL else None,
        ssl_certfile=settings.SSL_CERT_FILE if settings.USE_SSL else None,
    )