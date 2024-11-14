from fastapi import FastAPI
from src.db import engine
from alembic.config import Config
from alembic import command
from src.routers import posts, users

app = FastAPI()

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")

app.include_router(posts.router)
app.include_router(users.router)
