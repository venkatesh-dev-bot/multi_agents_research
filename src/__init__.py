"""
Market Research System package.
"""

from .main import MarketResearchSystem
from .models import (
	UseCase,
	Resource,
	IndustryAnalysis,
	ResearchResponse,
	MarketResponse,
	ResourceResponse,
	PriorityLevel,
	ComplexityLevel
)
from .agents.research_agent import ResearchAgent
from .agents.market_agent import MarketAgent
from .agents.resource_agent import ResourceAgent
from .utils.web_search import WebSearchTool

__version__ = "0.1.0"

__all__ = [
	'MarketResearchSystem',
	'UseCase',
	'Resource',
	'IndustryAnalysis',
	'ResearchResponse',
	'MarketResponse',
	'ResourceResponse',
	'PriorityLevel',
	'ComplexityLevel',
	'ResearchAgent',
	'MarketAgent',
	'ResourceAgent',
	'WebSearchTool'
]