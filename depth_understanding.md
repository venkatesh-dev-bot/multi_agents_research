# Market Research System - Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [Technical Architecture](#technical-architecture)
3. [Code Implementation Details](#code-implementation-details)
4. [Setup and Installation](#setup-and-installation)
5. [Usage Guide](#usage-guide)
6. [API Reference](#api-reference)
7. [Error Handling](#error-handling)
8. [Dependencies](#dependencies)
9. [Examples](#examples)

## System Overview

The Market Research System is an AI-powered platform that leverages multiple specialized agents to analyze companies and industries. The system provides comprehensive insights through three main components:
- Industry Analysis
- AI/ML Use Cases
- Implementation Resources

### Key Features
- Multi-agent architecture for specialized analysis
- Real-time web research capabilities
- Conversation memory for context retention
- Error handling and recovery mechanisms
- Configurable analysis parameters

## Technical Architecture

### Component Breakdown

1. **Main System (src/main.py)**
```python
class MarketResearchSystem:
    def __init__(self):
        self.research_agent = create_research_agent()
        self.market_agent = create_market_agent()
        self.resource_agent = create_resource_agent()
```
- Centralizes agent management
- Coordinates analysis workflows
- Handles response aggregation

2. **Research Agent (src/agents/research_agent.py)**
```python
class ResearchAgent(BaseAgent):
    def _get_prompt_template(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            ("system", """You are an expert research analyst..."""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])
```
- Specializes in company and industry analysis
- Implements web search capabilities
- Maintains conversation history

3. **Market Agent (src/agents/market_agent.py)**
- Focuses on AI/ML use case identification
- Evaluates technological opportunities
- Assesses market potential

4. **Resource Agent (src/agents/resource_agent.py)**
- Gathers implementation resources
- Provides practical guidance
- Identifies relevant tools and technologies

## Code Implementation Details

### 1. Main System Implementation

```python
def analyze_company(self, company_name: str, industry: str) -> dict:
    """
    Analyze a company using all agents.
    
    Args:
        company_name: Name of the company to analyze
        industry: Industry of the company
        
    Returns:
        dict: Analysis results including research, market, and resource data
    """
    # Research Analysis
    research_prompt = f"Analyze the company {company_name} in the {industry} industry"
    research_response = research_agent_response(self.research_agent, research_prompt)
    
    # Market Analysis
    market_prompt = f"Generate AI/ML use cases for {company_name} in {industry}"
    market_response = market_agent_response(self.market_agent, market_prompt)
    
    # Resource Analysis
    resource_prompt = f"Find implementation resources for {company_name} in {industry}"
    resource_response = resource_agent_response(self.resource_agent, resource_prompt)

    return {
        "industry_analysis": research_response,
        "use_cases": market_response,
        "resources": resource_response,
    }
```

### 2. Agent Implementation

```python
def create_research_agent() -> AgentExecutor:
    """Create a research agent for analyzing companies and industries."""
    
    # API Key Validation
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    # LLM Configuration
    llm = ChatOpenAI(
        model_name=MODEL_NAME,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=MAX_TOKENS
    )
    
    # Tool Setup
    search = DuckDuckGoSearchAPIWrapper()
    tools = [
        Tool(
            name="web_search",
            func=search.run,
            description="Search the web for information"
        )
    ]
    
    # Agent Creation
    agent = create_openai_functions_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # Memory Setup
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
        handle_parsing_errors=True,
    )
```

## Setup and Installation

1. **Prerequisites**
   - Python 3.8+
   - OpenAI API key
   - Git

2. **Installation Steps**
   ```bash
   # Clone repository
   git clone <repository-url>
   cd market-research-system

   # Install dependencies
   ./install_dev.sh

   # Set up environment variables
   export OPENAI_API_KEY='your-api-key'
   ```

3. **Configuration**
   - Update `config/constants.py` with desired parameters
   - Adjust memory settings if needed
   - Configure logging preferences

## Usage Guide

### Basic Usage
```python
from src.main import MarketResearchSystem

# Initialize system
system = MarketResearchSystem()

# Analyze company
results = system.analyze_company(
    company_name="Tesla",
    industry="Automotive"
)

# Access results
print("Industry Analysis:", results["industry_analysis"])
print("AI/ML Use Cases:", results["use_cases"])
print("Implementation Resources:", results["resources"])
```

### Advanced Usage
```python
# Custom configuration
system = MarketResearchSystem(
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=2000
)

# Batch analysis
companies = [
    ("Tesla", "Automotive"),
    ("Microsoft", "Technology"),
    ("JPMorgan", "Finance")
]

for company, industry in companies:
    results = system.analyze_company(company, industry)
    process_results(results)
```

## API Reference

### MarketResearchSystem

#### Methods
- `analyze_company(company_name: str, industry: str) -> dict`
  - Parameters:
    - company_name: Target company name
    - industry: Company's industry sector
  - Returns: Dictionary containing analysis results

#### Response Format
```python
{
    "industry_analysis": str,  # Research findings
    "use_cases": str,         # AI/ML applications
    "resources": str          # Implementation guidance
}
```

## Error Handling

1. **API Key Validation**
```python
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")
```

2. **Response Processing**
```python
try:
    response = agent.invoke({"input": prompt})
    return response["output"] if isinstance(response, dict) else str(response)
except Exception as e:
    print(f"Error getting response: {e}")
    return str(e)
```

## Dependencies

Required packages:
```
langchain==0.1.0
langchain_openai==0.1.0
langchain_core==0.1.0
langchain_community==0.1.0
python-dotenv==1.0.0
```

## Examples

### 1. Basic Company Analysis
```python
system = MarketResearchSystem()
results = system.analyze_company("Tesla", "Automotive")
```

### 2. Custom Configuration
```python
system = MarketResearchSystem()
system.configure(
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=2000
)
results = system.analyze_company("Microsoft", "Technology")
```

### 3. Error Handling
```python
try:
    results = system.analyze_company("Company", "Industry")
except ValueError as e:
    print(f"Configuration error: {e}")
except Exception as e:
    print(f"Analysis error: {e}")
```

## Best Practices

1. **API Key Management**
   - Use environment variables
   - Never hardcode sensitive data
   - Implement proper key rotation

2. **Resource Optimization**
   - Configure appropriate token limits
   - Implement rate limiting
   - Use caching when possible

3. **Error Handling**
   - Implement proper exception handling
   - Log errors appropriately
   - Provide meaningful error messages

4. **Memory Management**
   - Clear conversation history when appropriate
   - Monitor memory usage
   - Implement cleanup procedures

## Troubleshooting

Common issues and solutions:

1. **API Key Issues**
   - Verify environment variable setup
   - Check API key validity
   - Ensure proper permissions

2. **Response Timeout**
   - Adjust MAX_ITERATIONS setting
   - Check network connectivity
   - Verify rate limits

3. **Memory Issues**
   - Clear conversation history
   - Adjust buffer size
   - Monitor system resources

## Contributing

Guidelines for contributing to the project:

1. **Code Style**
   - Follow PEP 8 guidelines
   - Use meaningful variable names
   - Include proper documentation

2. **Testing**
   - Write unit tests
   - Include integration tests
   - Maintain test coverage

3. **Documentation**
   - Update relevant documentation
   - Include code examples
   - Maintain changelog

## Support

For additional support:

1. **Documentation**
   - Refer to this technical guide
   - Check the official documentation
   - Review code comments

2. **Community**
   - GitHub Issues
   - Discussion Forums
   - Stack Overflow

3. **Contact**
   - Technical Support
   - Development Team
   - Community Managers
