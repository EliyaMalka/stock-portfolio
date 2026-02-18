try:
    from langchain.agents import AgentExecutor
    print("Found in langchain.agents")
except ImportError:
    print("Not in langchain.agents")

try:
    from langchain.agents.agent import AgentExecutor
    print("Found in langchain.agents.agent")
except ImportError:
    print("Not in langchain.agents.agent")

import langchain
print(f"LangChain version: {langchain.__version__}")
