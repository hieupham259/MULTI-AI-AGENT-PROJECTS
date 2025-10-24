from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings

def get_response_from_ai_agents(model_name, system_prompt, messages, allow_search):

    llm = ChatGroq(model=model_name)

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    state = {"messages" : messages}

    response = agent.invoke(state)

    messages = response.get("messages")

    ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]

    return ai_messages[-1]