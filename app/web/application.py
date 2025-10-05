"""FastAPI application factory module.

This module contains the factory function for creating and configuring
the FastAPI application instance with all necessary extensions,
middleware, and routes.
"""

from fastapi import FastAPI
from fastapi.responses import UJSONResponse

from app.core.db.database import get_db_session
from app.core.extensions.cors_extension import enable_cors_extension
from app.core.extensions.exception_extension import enable_exception_extension
from app.core.extensions.logging_extension import enable_logging_extension
from app.core.extensions.route_extension import initialize_routes
from app.core.middleware.gzip_middleware import GZipMiddleware
from app.core.middleware.logging_middleware import LoggingMiddleware
from app.web.lifespan import lifespan_setup


def get_app() -> FastAPI:
    """Get FastAPI application.

    This is the main constructor of an application.

    :return: application.
    """
    app = FastAPI(
        version="1.0.0",
        title="Venture Vision FastAPI Backend",
        summary="FastAPI Backend Application",
        description="Venture Vision backend application created with FastAPI and PostgreSQL",
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/v1/openapi.json",
        default_response_class=UJSONResponse,
        contact={
            "name": "Paras Bhardava",
            "email": "parasbhardava26@gmail.com",
        },
        debug=False,
        lifespan=lifespan_setup,
    )

    # Main router for the API.
    initialize_routes(app)

    # Add CORS extension
    enable_cors_extension(app)

    # Add logging extension
    enable_logging_extension()

    # Add exception extension
    enable_exception_extension(app)

    # Add logging middleware
    app.add_middleware(LoggingMiddleware)

    # Add GZip middleware with minimum size threshold
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    app.dependency_overrides[get_db_session] = get_db_session
    return app
