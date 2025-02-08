from src.agents.research_agent import ResearchAgent
import streamlit as st
from dotenv import load_dotenv
import os
from typing import Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import the package modules
from src.agents.research_agent import ResearchAgent
from src.agents.market_agent import MarketAgent
from src.agents.resource_agent import ResourceAgent
from src.main import MarketResearchSystem


# Initialize agents
@st.cache_resource
def init_agents():
    try:
        research_agent = ResearchAgent()
        market_agent = MarketAgent()
        resource_agent = ResourceAgent()
        return research_agent, market_agent, resource_agent
    except Exception as e:
        logger.error(f"Error initializing agents: {e}")
        st.error(f"Error initializing agents: {e}")
        return None, None, None


# Initialize the system
@st.cache_resource
def get_system() -> Optional[MarketResearchSystem]:
    try:
        return MarketResearchSystem()
    except ImportError as e:
        logger.error(f"Failed to initialize system due to import error: {e}")
        st.error(f"Failed to initialize system due to import error: {e}")
        st.info("Please check your package versions in requirements.txt")
        return None
    except Exception as e:
        logger.error(f"Initialization error: {e}")
        st.error(f"Initialization error: {e}")
        st.info("Check your configuration and API key")
        return None

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="AI/ML Market Research System",
        page_icon="🔍",
        layout="wide"
    )
    
    # Header
    st.title("🔍 AI/ML Market Research System")
    st.markdown("""
    Generate AI/ML use cases and implementation resources for your company or industry.
    """)
    
    # Check for API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("Please set your OpenAI API key in the .env file")
        st.info("Copy .env.example to .env and add your OpenAI API key")
        st.code("cp .env.example .env", language="bash")
        return
    
    # Input form
    with st.form("research_form"):
        company_name = st.text_input("Company Name")
        industry = st.text_input("Industry")
        submit = st.form_submit_button("Generate Analysis")
    
    if submit:
        if not company_name or not industry:
            st.error("Please provide both company name and industry.")
            return
            
        try:
            with st.spinner("Initializing system..."):
                system = get_system()
                if system is None:
                    st.error("Failed to initialize the system. Please check your configuration.")
                    return
                
            with st.spinner("Analyzing company and industry..."):
                results = system.analyze_company(company_name, industry)
                
                # Display Results
                st.header("Industry Analysis")
                st.markdown(results["industry_analysis"])
                
                st.header("AI/ML Use Cases")
                st.markdown(results["use_cases"])
                
                st.header("Implementation Resources")
                st.markdown(results["resources"])
                
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error during analysis: {error_msg}")
            if "model_not_found" in error_msg:
                st.error("Error: The specified model is not available.")
                st.info("The system will use an alternative model. Please try again.")
            elif "invalid_request_error" in error_msg:
                try:
                    error_data = json.loads(error_msg.split(" - ")[-1].replace("'", '"'))
                    st.error(f"Error: {error_data['error']['message']}")
                except:
                    st.error(f"An error occurred: {error_msg}")
            else:
                st.error(f"An error occurred: {error_msg}")
                st.info("Please check the logs for more details.") 

if __name__ == "__main__":
    main()
