"""
Root Curation Agent - Coordinates all sub-agents for comprehensive company evaluation.
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from app.web.settings import settings
from app.agents.curation_agent.root_agent.prompt import ROOT_AGENT_PROMPT
from app.agents.curation_agent.founders_profile_agent.agent import founders_profile_agent
from app.agents.curation_agent.problem_market_size_agent.agent import problem_market_size_agent
from app.agents.curation_agent.unique_differentiator_finding_agent.agent import unique_differentiator_finding_agent
from app.agents.curation_agent.traction_and_metrics_agent.agent import traction_and_metrics_agent

root_agent = Agent(
    model=settings.model,
    name="root_agent",
    description="A comprehensive investment evaluation agent that coordinates specialized sub-agents to analyze companies across traction, differentiation, market opportunity, and founder capabilities.",
    instruction=ROOT_AGENT_PROMPT,
    tools=[
        AgentTool(agent=founders_profile_agent),
        AgentTool(agent=problem_market_size_agent),
        AgentTool(agent=unique_differentiator_finding_agent),
        AgentTool(agent=traction_and_metrics_agent),
        AgentTool(agent=web_search_agent),
    ],
)
