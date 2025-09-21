from pydantic import BaseModel, Field


class CompanyEvaluationRequest(BaseModel):
    """Request schema for company evaluation."""
    
    company_name: str = Field(..., description="Name of the company to evaluate", min_length=1)


class CompanyEvaluationResponse(BaseModel):
    """Response schema for company evaluation."""
    
    company_name: str
    final_report: str
    founders_profile_agent_response: str
    problem_market_size_agent_response: str
    unique_differentiator_agent_response: str
    traction_metrics_agent_response: str