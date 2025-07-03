from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
import logging

from api.v1.endpoints import posts
from models.models import Post
from database import engine
from sqlmodel import SQLModel
from sqlalchemy import event
from sqlalchemy.schema import CreateSchema

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_db_and_tables():
    # Ensure the schema exists before creating tables
    with engine.connect() as connection:
        connection.execute(CreateSchema("blogs", if_not_exists=True))
        connection.commit()
    SQLModel.metadata.create_all(engine)

# Call this function when the application starts
create_db_and_tables()

app = FastAPI(
    title="Blog Service API",
    description="A RESTful API for managing blog posts.",
    version="1.0.0",
)

origins = [
    "http://localhost",
    "http://localhost:5173", 
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*", "OPTIONS"],
    allow_headers=["*"],
)

@app.options("/{full_path:path}")
async def options_route(full_path: str):
    return {"message": "OK"}

app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Outgoing response: {request.method} {request.url} - Status: {response.status_code}")
    return response

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc.errors()} for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    logger.error(f"Pydantic validation error: {exc.errors()} for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    logger.error(f"An unexpected error occurred: {exc} for request: {request.url}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred."},
    )

@app.get("/")
async def root():
    return {"message": "Welcome to the Blog Service API"}