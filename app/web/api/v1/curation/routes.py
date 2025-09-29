"""This module contains the routes for the curation endpoints.

Functions:
    evaluate_company: Evaluates a company using the root curation agent.
"""

import json
import types
import uuid
from app.core.security.dependancies import RequireAdminKey
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from app.core.schema.curation_schema import CompanyEvaluationRequest,  CompanyEvaluationResponse
from google.genai import types

# DatabaseSessionService is imported inline for better error handling
from google.adk.runners import Runner
from app.core.schema.api_schema import create_json_api_response
from app.agents.curation_agent import root_agent
from loguru import logger


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
        
    runner = None
    try:
        # Update the root agent with the specific company name
        company_name = request.company_name.strip()
        print(company_name)
            
        # Set up session_service for the conversation
        # This manages the conversation state and context
        # Use DatabaseSessionService with SQLite for proper output_key handling
        from google.adk.sessions import DatabaseSessionService
        import os
        
        # Create SQLite database path
        db_path = os.path.join(os.getcwd(), "adk_sessions.db")
        sqlite_url = f"sqlite:///{db_path}"
        session_service = DatabaseSessionService(sqlite_url)
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
        logger.info(f"Starting company evaluation for: {company_name}")
        
        response = None
        async for event in runner.run_async(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=new_message,
        ):
            logger.debug(f"Event: {event}")
            
            if event.is_final_response():
                if event.content and event.content.parts:
                    response_text = str(event.content.parts[0].text)
                    response_text = response_text.replace("```json", "").replace("```", "").strip()
                    try:
                        print("RESPONSE TEXT", response_text)
                        response = json.loads(response_text)
                        break
                    except json.JSONDecodeError as json_error:
                        logger.error(f"JSON parse error: {json_error}")
                        raise HTTPException(
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Agent response format error: {str(json_error)}"
                        )
                        
            elif event.actions and event.actions.escalate:
                logger.warning("Agent escalation occurred")
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Agent escalation - unable to process the company evaluation request"
                )
                
        # If we reach here without a response, it's an incomplete execution
        if response is None:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Agent execution completed without generating a response"
            )
        
        print(response)
        return create_json_api_response(
            data=response,
            message=f"Successfully evaluated company: {company_name}",
            status_code=status.HTTP_200_OK
        )
        
    except Exception as e:
        logger.error(f"Error evaluating company: {e}")
        logger.exception("Full error details:")  # This will log the full traceback
        return create_json_api_response(
            message="Failed to evaluate company",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            errors=[{
                "code": "EVALUATION_ERROR", 
                "details": str(e)
            }]
        )
    finally:
        # Ensure runner is always closed
        if runner:
            try:
                await runner.close()
            except Exception as cleanup_error:
                logger.error(f"Error closing runner: {cleanup_error}")

