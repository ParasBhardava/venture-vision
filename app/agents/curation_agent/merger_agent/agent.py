"""
Root Curation Agent - Coordinates all sub-agents for comprehensive company evaluation.
"""

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from app.web.settings import settings
from app.agents.curation_agent.merger_agent.prompt import MERGER_AGENT_PROMPT

merger_agent = Agent(
    model=LiteLlm(model=f"{settings.provider}/{settings.model}", 
                  api_key=settings.google_api_key), 
    name="merger_agent",
    description="A comprehensive investment evaluation agent that coordinates specialized sub-agents to analyze companies across traction, differentiation, market opportunity, and founder capabilities.",
    instruction=MERGER_AGENT_PROMPT,
)
