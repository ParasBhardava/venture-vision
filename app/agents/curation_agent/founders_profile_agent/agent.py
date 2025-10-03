"""
This agent is responsible for researching and profiling startup founders and entrepreneurs.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from app.tools import parallel_mcp_toolset
from app.web.settings import settings
from app.agents.curation_agent.founders_profile_agent.prompt import FOUNDERS_PROFILE_AGENT_PROMPT

founders_profile_agent = Agent(
    model=LiteLlm(model=f"{settings.provider}/{settings.model}", api_key=settings.google_api_key),
    name="founders_profile_agent",  
    description="An agent specialized in researching and profiling startup founders and entrepreneurs.",
    instruction=FOUNDERS_PROFILE_AGENT_PROMPT,
    tools=[parallel_mcp_toolset],
    output_key="founders_profile_agent_result",
)
