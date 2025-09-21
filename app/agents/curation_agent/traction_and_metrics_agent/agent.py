"""
This agent is responsible for analyzing company traction, revenue figures, business metrics, customer acquisition costs, and marketing performance.
"""

from google.adk.agents import Agent
from app.tools import mcp_toolset
from app.agents.curation_agent.traction_and_metrics_agent.prompt import TRACTION_AND_METRICS_AGENT_PROMPT
from app.web.settings import settings


traction_and_metrics_agent = Agent(
    model=settings.model,
    name="traction_and_metrics_agent",
    description="An agent specialized in analyzing company traction, revenue breakdown, customer acquisition costs, marketing performance, operational efficiency, and business metrics for investment evaluation.",
    instruction=TRACTION_AND_METRICS_AGENT_PROMPT,
    tools=[mcp_toolset],
) 