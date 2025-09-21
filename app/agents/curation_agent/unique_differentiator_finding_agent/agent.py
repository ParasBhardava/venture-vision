"""
This agent is responsible for analyzing unique differentiators and competitive advantages for startups and business opportunities.
"""

from google.adk.agents import Agent
from app.tools import mcp_toolset
from app.agents.curation_agent.unique_differentiator_finding_agent.prompt import UNIQUE_DIFFERENTIATOR_FINDING_AGENT_PROMPT
from app.web.settings import settings


unique_differentiator_finding_agent = Agent(
    model=settings.model,
    name="unique_differentiator_finding_agent",
    description="An agent specialized in identifying and analyzing unique differentiators, competitive advantages, and sustainable competitive moats for businesses.",
    instruction=UNIQUE_DIFFERENTIATOR_FINDING_AGENT_PROMPT,
    tools=[mcp_toolset],
) 