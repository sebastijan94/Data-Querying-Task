"""
Main entry point for the FastAPI application.

This script initializes the FastAPI app, applies database migrations using Alembic,
and includes the application's API routers for handling different endpoint groups.
"""

from fastapi import FastAPI
from src.db import engine
from alembic.config import Config
from alembic import command
from src.routers import posts, users

app = FastAPI()

# Apply database migrations on startup to ensure the database is up-to-date.
alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

# Include routers for modular endpoint management
app.include_router(posts.router)
app.include_router(users.router)
