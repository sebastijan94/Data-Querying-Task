"""
Database setup and session management.

This module configures database connection settings using SQLAlchemy.
It provides both synchronous and asynchronous database options for use with FastAPI.
"""

from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Synchronous SQLAlchemy engine and session factory
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Async database instance
database = Database(DATABASE_URL)

def get_db():
    """Yields a database session for request handling, ensuring closure after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
