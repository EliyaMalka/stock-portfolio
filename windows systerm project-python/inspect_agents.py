import langchain.agents
print(dir(langchain.agents))
try:
    from langchain.agents import create_react_agent
    print("Found create_react_agent")
except ImportError:
    print("Not found create_react_agent")
