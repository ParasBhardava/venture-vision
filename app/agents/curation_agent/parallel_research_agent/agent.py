"""
Parallel Research Agent - Conducts parallel research on multiple companies.
"""

from google.adk.agents import ParallelAgent
from app.agents.curation_agent.founders_profile_agent import founders_profile_agent
from app.agents.curation_agent.problem_market_size_agent import problem_market_size_agent
from app.agents.curation_agent.unique_differentiator_finding_agent import unique_differentiator_finding_agent
from app.agents.curation_agent.traction_and_metrics_agent import traction_and_metrics_agent


parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    description="Runs multiple research agents in parallel to gather information for startup evaluation",
    sub_agents=[
        founders_profile_agent,
        problem_market_size_agent,
        unique_differentiator_finding_agent,
        traction_and_metrics_agent,
    ],
)
