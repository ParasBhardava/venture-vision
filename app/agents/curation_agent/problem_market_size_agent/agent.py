"""
This agent is responsible for analyzing the problem validation and market size assessment for startups and business opportunities.
"""

from google.adk.agents import Agent
from app.web.settings import settings
from google.adk.models.lite_llm import LiteLlm
from app.tools import parallel_mcp_toolset
from app.agents.curation_agent.problem_market_size_agent.prompt import PROBLEM_MARKET_SIZE_AGENT_PROMPT


problem_market_size_agent = Agent(
    model=LiteLlm(model=f"{settings.provider}/{settings.model}", 
                  api_key=settings.google_api_key),
    name="problem_market_size_agent",
    description="An agent specialized in problem validation, risk assessment, competitive analysis, and comprehensive market size analysis including TAM, SAM, and SOM calculations.",
    instruction=PROBLEM_MARKET_SIZE_AGENT_PROMPT,
    tools=[parallel_mcp_toolset],
    output_key="problem_market_size_agent_result",
) 