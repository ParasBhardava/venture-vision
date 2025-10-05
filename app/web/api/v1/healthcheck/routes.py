"""This module contains the views for the healthcheck endpoint.

Functions:
    healthcheck: Returns a simple healthcheck response.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.core.schema.api_schema import create_json_api_response


router = APIRouter(tags=["Healthcheck"])


@router.get("")
async def healthcheck() -> JSONResponse:
    """Checks the health of the application.

    Returns:
        JSONResponse: A JSON response indicating the health status.
    """
    return create_json_api_response(
        message="Healthcheck successful!",
        status_code=status.HTTP_200_OK,
    )
