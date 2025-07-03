# Blog Service API

This is a RESTful API for managing blog posts, built with Python and FastAPI. It provides comprehensive CRUD operations for blog posts and uses PostgreSQL as the database, containerized with Docker.

## Features

*   **CRUD Operations:** Create, Read, Update, and Delete blog posts.
*   **FastAPI:** High-performance web framework.
*   **PostgreSQL:** Relational database for data storage.
*   **Docker:** Containerization for easy setup and deployment.
*   **Pydantic:** Data validation and serialization.
*   **SQLAlchemy:** ORM for database interactions.
*   **Unit Tests:** Comprehensive test suite.
*   **Error Handling & Logging:** Robust error management and event tracking.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [repository_url]
    cd blog_service
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On macOS/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## How to Run

### Using Docker

1.  Ensure Docker is installed and running.
2.  Navigate to the `blog_service` directory.
3.  Run the command:
    ```bash
    docker compose up --build
    ```
    This will start the PostgreSQL database and the FastAPI application.

### Without Docker

1.  Ensure you have Python and `uvicorn` installed (via `requirements.txt`).
2.  Activate your virtual environment (if not already active).
3.  Run the application:
    ```bash
    uvicorn main:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## Configuration Details

The application uses environment variables for configuration, typically managed via a `.env` file. Ensure you have a `.env` file in the root directory with the necessary database credentials and other settings. Refer to `.env.example` for a template.

**Important Note:** Remember to copy `.env.example` to `.env` and fill in the necessary credentials.

## Project Structure

```
blog_service_api/
├── .venv/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── config.py
├── models/
│   └── models.py
├── schemas/
│   └── schemas.py
├── crud/
│   └── crud.py
├── api/
│   └── v1/
│       └── endpoints/
│           └── posts.py
├── tests/
│   ├── test_main.py
│   └── test_api.py
├── Dockerfile
└── docker-compose.yml
```

## API Documentation

Once the application is running, the interactive API documentation (Swagger UI) will be available at `/docs` and ReDoc at `/redoc`.