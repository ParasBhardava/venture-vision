"""
Root Curation Agent - Coordinates all sub-agents for comprehensive company evaluation.
"""

from google.adk.agents import SequentialAgent
from app.agents.curation_agent.founders_profile_agent import founders_profile_agent
from app.agents.curation_agent.merger_agent import merger_agent

# Test just founders_profile_agent + merger_agent to see output_key behavior
root_agent = SequentialAgent(   
    name="root_agent",
    description="Test founders agent output_key then merger agent",
    sub_agents = [founders_profile_agent, merger_agent],
)
