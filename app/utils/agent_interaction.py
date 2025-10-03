"""This module contains the functions for interacting with the agents.

Functions:
    call_agent_async: Process a user query through the agent asynchronously.
"""

import json
import os
import uuid
from typing import Any
from loguru import logger
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from google.adk.agents import Agent
from fastapi.responses import JSONResponse
from app.web.settings import settings

async def call_agent_async(agent: Agent, query: str, session_id: str = None, user_id: str = None) -> dict[str, Any]:
    """Process a user query through the agent asynchronously.
    
    Args:
        query (str): The user query to process.

    Returns:
        dict: Structured response with all agent results.
    """
    
    try:
        if session_id is None:
            session_id = str(uuid.uuid4())
        if user_id is None:
            user_id = str(uuid.uuid4())
    
        # Create the database session service
        db_path = os.path.join(os.getcwd(), settings.db_path)
        sqlite_url = f"sqlite:///{db_path}"
        session_service = DatabaseSessionService(db_url=sqlite_url)
        
        # Create the initial session state
        initial_session = {
            "company_name": query
        }
        
        # Create the session
        await session_service.create_session(
            app_name=settings.application_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_session,
        )
        
        # Set up the runner with root agent
        # The root agent decides which specialized agent should handle the response
        runner = Runner(
            agent = agent,
            app_name=settings.application_name,
            session_service=session_service
        )
        
        # Create content from the user query
        content = types.Content(
            role="user", parts=[types.Part.from_text(text=query)]
        )
        
        # Get the session to see state before processing
        session = await session_service.get_session(
            app_name=settings.application_name,
            user_id=user_id,
            session_id=session_id
        )
        
        logger.info(f"State before processing: {session.state}")

        # Run the agent with the user query
        events = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=content
        )
        
        # Get the final response from the agent
        final_response = {
            "final_report": "No final report generated",
            "founders_profile_agent_response":  "No data available",
            "problem_market_size_agent_response": "No data available",
            "unique_differentiator_agent_response": "No data available",
            "traction_metrics_agent_response": "No data available",
            "merger_agent_response": "No data available"
        }
        
        
        async for event in events:
            logger.info(f"Received event: {type(event).__name__}")
            logger.info(f"Event: {event}")
            if event.content and event.content.parts:   
                final_response = event.content.parts[0].text
                

        # Get updated session to see state after processing
        session = await session_service.get_session(
            app_name=settings.application_name,
            user_id=user_id,
            session_id=session_id
        )        
        logger.info(f"State after processing: {session.state}")

        final_response = final_response.replace("```json", "").replace("```", "")
        logger.info(f"Final response: {final_response}")
        return final_response
    
    except Exception as e:
        import traceback
        logger.error(f"Error while executing agent: {e}")
        logger.error(f"Exception type: {type(e).__name__}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise e
