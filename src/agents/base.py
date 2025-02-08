from typing import Tuple
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor
from langchain.agents import create_openai_functions_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain.memory import ConversationBufferMemory
from ..config.constants import *

class BaseAgent:
    """Base class for all agents in the system."""
    
    def __init__(self):
        """Initialize base agent with common components."""
        self.llm = self._init_llm()
        self.tools = self._setup_tools()
        self.memory = self._setup_memory()
        self.agent_executor = self._create_agent()
    
    def _init_llm(self) -> ChatOpenAI:
        """Initialize the language model."""
        return ChatOpenAI(
            model_name=MODEL_NAME,
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=MAX_TOKENS
        )
    
    def _setup_tools(self) -> list[Tool]:
        """Setup agent tools. Override in specialized agents."""
        search = DuckDuckGoSearchAPIWrapper()
        return [
            Tool(
                name="web_search",
                func=search.run,
                description="Search the web for information"
            )
        ]
    
    def _setup_memory(self) -> ConversationBufferMemory:
        """Setup conversation memory."""
        return ConversationBufferMemory(
            return_messages=True,
            memory_key="chat_history",
            output_key="output"
        )
    
    def _create_agent(self) -> AgentExecutor:
        """Create the agent executor."""
        prompt = self._get_prompt_template()
        agent = create_openai_functions_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt
        )
        
        return AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=VERBOSE,
            max_iterations=MAX_ITERATIONS,
            handle_parsing_errors=True
        )
    
    def _get_prompt_template(self) -> ChatPromptTemplate:
        """Get the prompt template. Override in specialized agents."""
        return ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant."),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
    
    def get_response(self, prompt: str) -> str:
        """Get response from agent without cost tracking."""
        try:
            response = self.agent_executor.invoke({"input": prompt})
            return response["output"] if isinstance(response, dict) else str(response)
        except Exception as e:
            error_msg = f"Error getting response: {e}"
            print(error_msg)
            return error_msg 