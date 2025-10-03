"""Curation API module for company evaluation and analysis.

This module exports the curation router which provides endpoints
for analyzing companies using the root curation agent.
"""

from app.web.api.v1.curation.routes import router as curation_router


__all__ = ["curation_router"] 