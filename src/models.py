from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class PriorityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class ComplexityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

class UseCase(BaseModel):
    title: str = Field(..., description="Title of the use case")
    description: str = Field(..., description="Detailed description of the use case")
    priority: PriorityLevel = Field(..., description="Priority level (High/Medium/Low)")
    complexity: ComplexityLevel = Field(..., description="Implementation complexity (High/Medium/Low)")
    expected_impact: str = Field(..., description="Expected business impact")

class Resource(BaseModel):
    title: str = Field(..., description="Title of the resource")
    url: str = Field(..., description="URL or source of the resource")
    description: str = Field(..., description="Description of the resource")
    quality_assessment: str = Field(..., description="Brief assessment of resource quality")

class IndustryAnalysis(BaseModel):
    overview: str = Field(..., description="Industry overview and current state")
    key_players: List[str] = Field(..., description="List of key players in the industry")
    tech_trends: List[str] = Field(..., description="Technology adoption trends")
    opportunities: List[str] = Field(..., description="Market opportunities")
    challenges: List[str] = Field(..., description="Key challenges and risks")

class ResearchResponse(BaseModel):
    industry_analysis: IndustryAnalysis = Field(..., description="Detailed industry analysis")

class MarketResponse(BaseModel):
    use_cases: List[UseCase] = Field(..., description="List of AI/ML use cases")

class ResourceResponse(BaseModel):
    resources: List[Resource] = Field(..., description="List of implementation resources") 