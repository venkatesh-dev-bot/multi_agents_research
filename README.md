# Market Research & Use Case Generation System

A multi-agent system for generating AI/ML use cases and implementation resources for companies and industries.

## Features

- 🔍 Industry and Company Analysis
- 🤖 AI/ML Use Case Generation
- 📚 Implementation Resource Collection
- 🌐 Web-based Interface

## Architecture

The system uses a multi-agent architecture with three specialized agents:

1. **Research Agent**: Analyzes industry and company information
2. **Market Agent**: Generates relevant AI/ML use cases
3. **Resource Agent**: Collects implementation resources

For detailed architecture information, see [docs/architecture.md](docs/architecture.md).

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/market-research-system.git
cd market-research-system
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` with your API key:
```bash
OPENAI_API_KEY=your_openai_key
```

## Usage

### Running the Streamlit Interface

```bash
streamlit run run.py
```

This will open the web interface where you can:
1. Enter company/industry information
2. Generate analysis and use cases
3. View implementation resources

### Using the Python API

```python
# Initialize the system
system = MarketResearchSystem()

# Run analysis
results = system.analyze_company(
    company_name="Your Company",
    industry="Your Industry"
)

# Access results
print(results["industry_analysis"])
print(results["use_cases"])
print(results["resources"])
```

## Project Structure

```
market_research_system/
├── src/
│   ├── agents/
│   │   ├── __init__.py        
│   │   ├── base.py           # Base agent class with common functionality
│   │   ├── research_agent.py # Industry analysis agent
│   │   ├── market_agent.py   # Use case generation agent
│   │   └── resource_agent.py # Implementation resources agent
│   ├── utils/
│   │   ├── __init__.py        
│   │   ├── web_search.py     # Web search utilities
│   ├── config/
│   │   ├── __init__.py        
│   │   └── constants.py      # System configuration
│   └── interface/
│   │   ├── __init__.py        
│       └── streamlit_app.py   # Web interface
│── __init__.py
│── main.py
│── models.py
│── run.py  

```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI GPT-4o-mini for language model capabilities
- Streamlit for the web interface
- DuckDuckGo for search capabilities 
