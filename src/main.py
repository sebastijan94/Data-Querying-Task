from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from src.db import engine
from alembic.config import Config
from alembic import command
from src.routers import posts, users
from contextlib import asynccontextmanager

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

app = FastAPI()

try:
    with engine.connect() as conn:
        run_migrations()
except OperationalError:
    print("Database connection failed. Ensure the database is running.")

app.include_router(posts.router)
app.include_router(users.router)
