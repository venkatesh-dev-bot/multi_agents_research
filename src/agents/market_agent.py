import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor
from langchain.agents import create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
from typing import Dict

from ..config.constants import *
from .base import BaseAgent


class MarketAgent(BaseAgent):
    """Market agent for generating AI/ML use cases."""
    
    def _get_prompt_template(self) -> ChatPromptTemplate:
        """Get the specialized prompt template for market analysis."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert in AI/ML solutions and market analysis. 
            Your task is to analyze industry trends for AI/ML adoption, generate relevant use cases based on company/industry needs, 
            prioritize use cases based on impact and feasibility, and consider implementation complexity.
            
            To search for information, use the web_search tool."""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])


def create_market_agent() -> AgentExecutor:
    """Create a market analysis agent for generating AI/ML use cases."""
    
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    
    search = DuckDuckGoSearchAPIWrapper()
    
    tools = [
        Tool(
            name="web_search",
            func=search.run,
            description="Search for AI/ML use cases and market trends"
        )
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in AI/ML solutions and market analysis. 
        Your task is to analyze industry trends for AI/ML adoption, generate relevant use cases based on company/industry needs, 
        prioritize use cases based on impact and feasibility, and consider implementation complexity.
        
        To search for information, use the web_search tool."""),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])
    
    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="output"
    )
    
    return AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=VERBOSE,
        max_iterations=MAX_ITERATIONS,
        handle_parsing_errors=True
    )


def get_agent_response(agent: AgentExecutor, prompt: str) -> str:
    """Get response from agent without cost tracking."""
    try:
        response = agent.invoke({"input": prompt})
        return response["output"] if isinstance(response, dict) else str(response)
    except Exception as e:
        print(f"Error getting response: {e}")
        return str(e)


def analyze_use_case(title: str, description: str, industry_data: Dict) -> Dict:
    """Analyze and score a potential use case."""
    challenges = industry_data.get("challenges", [])
    
    priority = "High" if any(c.lower() in description.lower() for c in challenges) else "Medium"
    
    complexity_indicators = {
        "data": "High",
        "automation": "Medium",
        "customer": "Medium",
        "security": "High",
        "analytics": "Medium",
        "prediction": "High"
    }
    
    complexity = "Medium"
    for indicator, level in complexity_indicators.items():
        if indicator in description.lower():
            complexity = level
            break
    
    return {
        "title": title,
        "description": description,
        "priority": priority,
        "complexity": complexity,
        "expected_impact": "High",
        "implementation_timeline": "3-6 months",
        "key_requirements": [
            "Data collection and preparation",
            "Model development and training",
            "Integration with existing systems",
            "Staff training and adoption"
        ]
    }
