"""Run script for the Market Research System."""

import os
import sys
from streamlit.web import cli as stcli

# Get the absolute path to the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the project root to Python path
sys.path.append(os.path.dirname(current_dir))

if __name__ == "__main__":
    # Get the path to the app.py file
    app_path = os.path.join(current_dir, "interface", "app.py")
    
    sys.argv = [
        "streamlit",
        "run",
        app_path,
        "--server.port=8501",
        "--server.address=0.0.0.0"
    ]
    stcli.main() 