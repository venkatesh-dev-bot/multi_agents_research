"""Main module for the Market Research System."""

from .agents.market_agent import get_agent_response as market_agent_response
from .agents.research_agent import get_agent_response as research_agent_response
from .agents.resource_agent import get_agent_response as resource_agent_response
from .agents import (
    create_research_agent,
    create_market_agent,
    create_resource_agent
)

class MarketResearchSystem:
    """Main class for the Market Research System."""

    def __init__(self):
        """Initialize the Market Research System."""
        self.research_agent = create_research_agent()
        self.market_agent = create_market_agent()
        self.resource_agent = create_resource_agent()
        
    def analyze_company(self, company_name: str, industry: str) -> dict:
        """
        Analyze a company using all agents.
        
        Args:
            company_name: Name of the company to analyze
            industry: Industry of the company
            
        Returns:
            dict: Analysis results including research, market, and resource data
        """
        research_prompt = f"Analyze the company {company_name} in the {industry} industry"
        research_response = research_agent_response(self.research_agent, research_prompt)
        
        market_prompt = f"Generate AI/ML use cases for {company_name} in {industry}"
        market_response = market_agent_response(self.market_agent, market_prompt)
        
        resource_prompt = f"Find implementation resources for {company_name} in {industry}"
        resource_response = resource_agent_response(self.resource_agent, resource_prompt)

        return {
            "industry_analysis": research_response,
            "use_cases": market_response,
            "resources": resource_response,
        }
