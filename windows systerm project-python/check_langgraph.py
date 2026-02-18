try:
    from langgraph.prebuilt import create_react_agent
    print("Found create_react_agent in langgraph.prebuilt")
except ImportError:
    print("Not found in langgraph.prebuilt")

try:
    from langchain_ollama import ChatOllama
    print("Found ChatOllama")
except ImportError:
    print("Not found ChatOllama")
