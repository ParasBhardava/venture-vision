"""Lifespan management module for FastAPI application.

This module handles database connection setup and cleanup during application startup and shutdown.
It provides connection pooling and proper resource management for database interactions.
"""

import os
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from datetime import datetime
from google.adk.sessions import DatabaseSessionService
from fastapi import FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

from app.web.settings import settings


@asynccontextmanager
async def lifespan_setup(app: FastAPI) -> AsyncGenerator[None]:
    """Initialize database connections and cleanup on shutdown.

    Args:
        app (FastAPI): The FastAPI application instance

    Yields:
        None

    Raises:
        SQLAlchemyError: If database connection or table creation fails
    """
    startup_start_time = datetime.now()
    logger.info("Starting application initialization")

    # Create engine with proper configuration
    engine: AsyncEngine = create_async_engine(
        settings.postgres_database_url,
        pool_size=20,
        max_overflow=10,
        pool_recycle=3600,
        echo=settings.postgres_database_echo,
    )

    # Create session factory with explicit type
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    # Store in app state
    app.state.db_engine = engine
    app.state.db_session_factory = session_factory
    
    
    # Create the session service
    db_path = os.path.join(os.getcwd(), settings.db_path)
    sqlite_url = f"sqlite:///{db_path}"
    app.state.session_service = DatabaseSessionService(db_url=sqlite_url)


    startup_elapsed_time = (datetime.now() - startup_start_time).total_seconds()
    logger.info(f"Application initialization completed in {startup_elapsed_time:.2f}s")

    yield

    # Cleanup
    logger.info("Starting application shutdown")
    shutdown_start_time = datetime.now()

    try:
        await engine.dispose()
        logger.info("Database connections closed successfully")
    except Exception as e:
        logger.error(f"Error during database connection cleanup: {e!s}")

    shutdown_elapsed_time = (datetime.now() - shutdown_start_time).total_seconds()
    logger.info(f"Application shutdown completed in {shutdown_elapsed_time:.2f}s")
