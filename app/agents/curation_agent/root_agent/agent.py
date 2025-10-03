"""
Root Curation Agent - Coordinates all sub-agents for comprehensive company evaluation.
"""

from google.adk.agents import SequentialAgent
from app.agents.curation_agent.parallel_research_agent.agent import parallel_research_agent
from app.agents.curation_agent.merger_agent import merger_agent

# Test just founders_profile_agent + merger_agent to see output_key behavior
root_agent = SequentialAgent(   
    name="root_agent",
    description="Test founders agent output_key then merger agent",
    sub_agents = [parallel_research_agent, merger_agent],
)
