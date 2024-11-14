import logging
import os
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic import context
from src.base import Base
import src.models.models # noqa

# Load the .env file
from dotenv import load_dotenv
load_dotenv()

# Access the DATABASE_URL from the environment
config = context.config
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
)

# Used for 'autogenerate' support
target_metadata = Base.metadata

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
