from setuptools import setup, find_packages

setup(
    name="market-research-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "langchain-openai",
        "langchain-core",
        "langchain-community",
        "openai",
        "streamlit",
        "python-dotenv",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A multi-agent system for market research and AI/ML use case generation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
) 