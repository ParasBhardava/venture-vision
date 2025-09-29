"""
This agent is responsible for analyzing unique differentiators and competitive advantages for startups and business opportunities.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from app.tools import parallel_mcp_toolset
from app.agents.curation_agent.unique_differentiator_finding_agent.prompt import UNIQUE_DIFFERENTIATOR_FINDING_AGENT_PROMPT
from app.web.settings import settings


unique_differentiator_finding_agent = Agent(
    model=LiteLlm(model=f"{settings.provider}/{settings.model}", 
                  api_key=settings.google_api_key),
    name="unique_differentiator_finding_agent",
    description="An agent specialized in identifying and analyzing unique differentiators, competitive advantages, and sustainable competitive moats for businesses.",
    instruction=UNIQUE_DIFFERENTIATOR_FINDING_AGENT_PROMPT,
    tools=[parallel_mcp_toolset],
    output_key="unique_differentiator_finding_agent_result",
) 