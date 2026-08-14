import os
import logging
from fastapi import FastAPI, Depends, Request, Response, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from database import engine, get_db
import models

# Auto-create SQLite database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Import routers from app/routes directory
from app.routes.events import router as events_router
from app.routes.post import router as post_router
from app.routes.analyze import router as analyze_router
from app.routes.alerts import router as alerts_router
from app.routes.stats import router as stats_router

logger = logging.getLogger("sentinel_backend")

# Initialize the FastAPI application
app = FastAPI(
 from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

 title="Sentinel AI API",
    description="Backend API for Sentinel AI hackathon project",
    version="0.1.0"
)

# Task 1: Define allowed origins for local frontend development (React, Vite, Vue, etc.)
# Allows environment variable override via CORS_ORIGINS
default_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8080",
]

cors_env = os.getenv("CORS_ORIGINS")
if cors_env:
    origins = [origin.strip() for origin in cors_env.split(",") if origin.strip()]
else:
    origins = default_origins

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Task 2: Global Exception Handler for database errors (safe response without exposing internal traces)
@app.exception_handler(SQLAlchemyError)
def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A database error occurred. Internal details have been hidden for security."}
    )


# Task 2: Global Exception Handler for generic unhandled server errors
@app.exception_handler(Exception)
def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled server error on {request.url.path}: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )


# Register routers using app.include_router()
app.include_router(events_router)
app.include_router(post_router)
app.include_router(analyze_router)
app.include_router(alerts_router)
app.include_router(stats_router)


# Task 3: Improved Health check endpoint (GET /health)
@app.get("/health", tags=["Health"])
def health_check(response: Response, db: Session = Depends(get_db)):
    """
    Health check endpoint verifying API server status and SQLite database connection.
    Returns HTTP 200 with status: healthy and database: connected if healthy,
    or HTTP 503 if database connectivity fails.
    """
    try:
        # Execute lightweight ping query to verify database is reachable
        db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected"
        }
    except Exception as exc:
        logger.error(f"Health check DB ping failed: {exc}")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {
            "status": "unhealthy",
            "database": "disconnected"
        }
