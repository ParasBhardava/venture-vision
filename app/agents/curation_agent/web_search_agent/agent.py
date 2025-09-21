"""
This agent is responsible for conducting comprehensive web research about companies and market intelligence.
"""

from google.adk.agents import Agent
from google.adk.tools import google_search
from app.web.settings import settings
from app.agents.curation_agent.web_search_agent.prompt import WEB_SEARCH_AGENT_PROMPT

web_search_agent = Agent(
    model=settings.model,
    name="web_search_agent",
    description="An agent specialized in conducting comprehensive web research about companies, market intelligence, and gathering detailed information from web sources.",
    instruction=WEB_SEARCH_AGENT_PROMPT,
    tools=[google_search],
) 