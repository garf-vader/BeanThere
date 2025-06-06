# app/core.py
import logging

from app.db.database import init_db  # Function to initialize DB
from app.routers import coffee  # Import routes
from app.routers import cafe
from app.routers import user
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

app = FastAPI(title="CoffeeAPI", version="0.0.0")

# Initialize database (this can be moved elsewhere if needed)
init_db()

# Include routers
app.include_router(coffee.router)
app.include_router(cafe.router)
app.include_router(user.router)


# Add exception handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )
