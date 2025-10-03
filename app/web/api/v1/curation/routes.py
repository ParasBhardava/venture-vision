"""This module contains the routes for the curation endpoints.

Functions:
    evaluate_company: Evaluates a company using the root curation agent.
"""

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.core.schema.curation_schema import CompanyEvaluationRequest
from app.core.schema.api_schema import create_json_api_response
from app.utils.agent_interaction import call_agent_async
from loguru import logger
from app.agents.curation_agent.root_agent.agent import root_agent
from app.core.security.dependancies import RequireAdminKey

router = APIRouter(tags=["Curation"])


@router.post("")
async def evaluate_company(request: CompanyEvaluationRequest, _: RequireAdminKey) -> JSONResponse:
    """Evaluates a company using the root curation agent.
    
    This endpoint analyzes a company using specialized sub-agents that examine:
    - Founders & Team Assessment
    - Market Opportunity & Problem Validation  
    - Competitive Advantage & Differentiation
    - Traction & Business Metrics Analysis
    
    Args:
        request: CompanyEvaluationRequest containing the company name to evaluate
        
    Returns:
        JSONResponse: Comprehensive company evaluation report
    """
    try:
        company_name = request.company_name.strip()
        logger.info(f"Evaluating company: {company_name}")
        response = await call_agent_async(root_agent, company_name)
        return create_json_api_response(
            data=response,
            message=f"Successfully evaluated company: {company_name}",
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error evaluating company: {e}")
        return create_json_api_response(
            message="Failed to evaluate company",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=[{
                "code": "EVALUATION_ERROR", 
                "details": str(e)
            }]
        )