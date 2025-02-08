from typing import List, Dict
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


class WebSearchTool:
    """Enhanced web search utility with result processing."""
    
    def __init__(self):
        """Initialize the search wrapper."""
        self.search = DuckDuckGoSearchAPIWrapper()
    
    def search_with_metadata(self, query: str, num_results: int = 5) -> List[Dict]:
        """
        Perform a web search and return structured results with metadata.
        
        Args:
            query: Search query string
            num_results: Number of results to return
            
        Returns:
            List of dictionaries containing search results with metadata
        """
        try:
            raw_results = self.search.run(query)
            
            # Process and structure the results
            processed_results = []
            for result in raw_results.split('\n')[:num_results]:
                if result.strip():
                    processed_results.append({
                        'content': result.strip(),
                        'query': query,
                        'source': 'DuckDuckGo'
                    })
            
            return processed_results
        except Exception as e:
            print(f"Error in web search: {e}")
            return []
    
    def run(self, query: str) -> str:
        """
        Simple search interface compatible with LangChain Tool format.
        
        Args:
            query: Search query string
            
        Returns:
            Search results as a string
        """
        try:
            return self.search.run(query)
        except Exception as e:
            print(f"Error in web search: {e}")
            return f"Error performing web search: {str(e)}" 