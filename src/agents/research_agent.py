import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor
from langchain.agents import create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.memory import ConversationBufferMemory

from ..config.constants import *
from .base import BaseAgent


class ResearchAgent(BaseAgent):
    """Research agent for analyzing companies and industries."""
    
    def _get_prompt_template(self) -> ChatPromptTemplate:
        """Get the specialized prompt template for research."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert research analyst specializing in AI/ML technologies. 
            Your task is to analyze companies and industries thoroughly, identify current offerings and capabilities, 
            evaluate technological maturity and readiness, and highlight key opportunities and challenges.
            
            To search for information, use the web_search tool."""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])


def create_research_agent() -> AgentExecutor:
    """Create a research agent for analyzing companies and industries."""
    
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
            description="Search the web for information about companies and industries"
        )
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert research analyst specializing in AI/ML technologies. 
        Your task is to analyze companies and industries thoroughly, identify current offerings and capabilities, 
        evaluate technological maturity and readiness, and highlight key opportunities and challenges.
        
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
