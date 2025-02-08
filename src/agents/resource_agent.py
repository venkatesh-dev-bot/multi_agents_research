import os
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor
from langchain.agents import create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.memory import ConversationBufferMemory

from ..config.constants import MODEL_NAME, DEFAULT_TEMPERATURE, MAX_TOKENS, MAX_ITERATIONS, VERBOSE
from .base import BaseAgent


class ResourceAgent(BaseAgent):
    """Resource agent for finding AI/ML implementation resources."""
    
    def _get_prompt_template(self) -> ChatPromptTemplate:
        """Get the specialized prompt template for resource finding."""
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert in finding and evaluating AI/ML implementation resources. 
            Your task is to find relevant tutorials, documentation, and example implementations, evaluate resource quality and applicability, 
            provide clear implementation guidance, and include links to GitHub repositories, documentation, and tutorials.
            
            To search for information, use the web_search tool."""),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])


def create_resource_agent() -> AgentExecutor:
    """Create a resource agent for finding AI/ML implementation resources."""
    
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
            description="Search for AI/ML implementation resources, tutorials, and documentation"
        )
    ]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert in finding and evaluating AI/ML implementation resources. 
        Your task is to find relevant tutorials, documentation, and example implementations, evaluate resource quality and applicability, 
        provide clear implementation guidance, and include links to GitHub repositories, documentation, and tutorials.
        
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
