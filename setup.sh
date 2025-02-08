#!/bin/bash

echo "Setting up Market Research System..."

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate || source venv/Scripts/activate

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Create project structure
mkdir -p src/agents src/tools
touch src/__init__.py
touch src/agents/__init__.py
touch src/tools/__init__.py

echo "Setup complete! Remember to:"
echo "1. Create .env file from .env.example"
echo "2. Add your API keys to .env"
echo "3. Activate virtual environment:"
echo "   source venv/bin/activate (Linux/macOS)"
echo "   or"
echo "   venv\Scripts\activate (Windows)" 