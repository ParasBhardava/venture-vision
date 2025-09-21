"""This module contains the routes for the curation endpoints.

Functions:
    evaluate_company: Evaluates a company using the root curation agent.
"""

import json
import types
import uuid
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from app.core.schema.curation_schema import CompanyEvaluationRequest,  CompanyEvaluationResponse
from google.genai import types

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from app.core.schema.api_schema import create_json_api_response
from app.agents.curation_agent.root_agent.agent import root_agent
from loguru import logger


router = APIRouter(tags=["Curation"])


@router.post("/")
async def evaluate_company(request: CompanyEvaluationRequest) -> JSONResponse:
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
        # Update the root agent with the specific company name
        company_name = request.company_name.strip()
        print(company_name)
            
        # Set up session_service for the conversation
        # This manages the conversation state and context
        session_service = InMemorySessionService()
        initial_session = {
            "company_name": company_name
        }

        # Generate unique identifiers for the google_adk session
        # These ensure each conversation is properly isolated
        APP_NAME = "Venture Vision"
        USER_ID = str(uuid.uuid4())
        SESSION_ID = str(uuid.uuid4())

        # Create the google_adk session with initial state
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID,
            state=initial_session,
        )

        # Set up the runner with root agent
        # The root agent decides which specialized agent should handle the response
        runner = Runner(
            agent= root_agent,
            app_name=APP_NAME,
            session_service=session_service
        )
        
        # Create the new message for processing
        new_message = types.Content(role="user", parts=[types.Part(text=company_name)])
        
        # Process the message through the agent system
        # This triggers the agent orchestration flow
        response = ("", "")
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            logger.debug(f"Event: {event}")
            # Return the final response when available
            if event.is_final_response():
                if event.content and event.content.parts:
                    print(event.content.parts)
                    response = str(event.content.parts[0].text)
                    response = response.replace("```json", "").replace("```", "").strip()
                    response = json.loads(response)
                    
            # Handle potential errors/escalations
            elif event.actions and event.actions.escalate: 
                response =  CompanyEvaluationResponse(
                    company_name=company_name,
                    final_report="No results found",
                    founders_profile_agent_response="No results found",
                    problem_market_size_agent_response="No results found",
                    unique_differentiator_agent_response="No results found",
                    traction_metrics_agent_response="No results found",
                )
                break   
        
    
        print(response)
        return create_json_api_response(
            data=response,
            message=f"Successfully evaluated company: {company_name}",
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        return create_json_api_response(
            message="Failed to evaluate company",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=[{
                "code": "EVALUATION_ERROR", 
                "details": str(e)
            }]
        )

