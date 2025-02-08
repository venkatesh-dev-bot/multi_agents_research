import os
import sys
from streamlit.web import cli as stcli

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the project root to Python path
sys.path.append(os.path.dirname(current_dir))

# Import the main function from the app module
from src.interface.app import main

if __name__ == "__main__":
    # Run the Streamlit app
    stcli.main()