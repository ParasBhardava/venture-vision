"""
This agent is responsible for researching and profiling startup founders and entrepreneurs.
"""

from google.adk.agents import Agent
from app.tools import mcp_toolset
from app.web.settings import settings
from app.agents.curation_agent.founders_profile_agent.prompt import FOUNDERS_PROFILE_AGENT_PROMPT

founders_profile_agent = Agent(
    model=settings.model,
    name="founders_profile_agent",
    description="An agent specialized in researching and profiling startup founders and entrepreneurs.",
    instruction=FOUNDERS_PROFILE_AGENT_PROMPT,
    tools=[mcp_toolset],
)
