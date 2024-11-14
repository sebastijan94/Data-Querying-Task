# Data Querying API

This is a FastAPI application designed to provide an efficient and flexible data querying mechanism with reusable endpoints. 
The app allows you to query for users and posts with optional inclusion of related data, such as tags, comments, and user details.

## Features

- Retrieve posts with optional inclusion of related fields (tags, user, comments).
- Retrieve users with optional inclusion of related fields (posts, comments).
- Production-ready, modular, and easily extensible design.

## Prerequisites

- **Docker**: To run the application and PostgreSQL database in isolated containers.
- **Python**: Version 3.9.19

## Project Setup

### 1. Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/sebastijan94/Data-Querying-Task.git
cd Data-Querying-Task
```

### 2. Environment Variables

Create a `.env` file in the root directory and define the `DATABASE_URL` variable for PostgreSQL. You can use following data:

```dotenv
DATABASE_URL=postgresql://db_user:secure_password123!@localhost/fastapi_app_db
```

### 3. Run PostgreSQL with Docker Compose

Docker Compose will handle setting up the PostgreSQL database.

```bash
docker compose up -d
```

### 4. Run the FastAPI Application

With the database running in Docker, you can now start the FastAPI app manually. The app will detect the database and run migrations on startup.

1. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the App**:

    ```bash
    uvicorn src.main:app --reload
    ```

### 5. Access the API

The app will run on `http://127.0.0.1:8000`. You can access the API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`

### 6. Run Tests

Tests are located in the `src/tests` directory and can be executed with `pytest`.

1. **Run Tests**:

    ```bash
    pytest src/tests
    ```

Tests use `unittest.mock` to simulate database interactions and ensure isolation. Each test checks various combinations of include fields (e.g., comments, tags, users) for the main API endpoints.

## Endpoints Overview

### 1. `/api/posts`

- `GET /api/posts`: Retrieve a list of posts with optional filters and inclusion of related fields.
    - Query parameters:
        - `status`: Filter posts by status (`published`, `draft`, `archived`).
        - `include`: Comma-separated list of related fields to include in the response (e.g., `tags,user,comments`).

- `GET /api/posts/{post_id}`: Retrieve a specific post by its ID, with optional inclusion of related fields.
    - Path parameter:
        - `post_id`: The ID of the post to retrieve.
    - Query parameter:
        - `include`: Comma-separated list of related fields to include in the response (e.g., `tags,user,comments`).

### 2. `/api/users`

- `GET /api/users/{user_id}`: Retrieve a user by ID with optional inclusion of related fields.
    - Path parameter:
        - `user_id`: The ID of the user to retrieve.
    - Query parameter:
        - `include`: Comma-separated list of related fields to include in the response (e.g., `posts,comments`).

## Additional Notes

- **Database Migrations**: Alembic is used for database migrations. Migrations are run automatically on startup.

This setup and structure allow for easy extension and flexibility in data querying. Each endpoint allows for conditional inclusion of related fields, providing efficient and targeted data responses.
