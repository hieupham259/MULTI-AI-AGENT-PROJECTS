from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults

from langchain.agents import create_agent
from langchain_core.messages.ai import AIMessage

from app.config.settings import settings


def get_response_from_ai_agents(model_name, system_prompt, messages, allow_search):
    llm = ChatGoogleGenerativeAI(
        api_key=settings.GEMINI_API_KEY,
        model=model_name
    )

    tools = [TavilySearchResults(max_results=5, topic="general")] if allow_search else []

    messages = [{"role": "user", "content": messages}]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=system_prompt
    )

    state = {"messages" : messages}

    response = agent.invoke(state)
    ai_response = "No response generated."

    messages = response.get("messages")

    # ai_messages = [message.content for message in messages if isinstance(message,AIMessage)]
    for message in messages: 
        if isinstance(message,AIMessage):
            content = message.content[-1]
            ai_response = content.get('text')
    return ai_response


if __name__ == "__main__":
    system_prompt = "You are a helpful machine learning assistant."
    # messages = [{"role": "user", "content": "Explain machine learning"}]
    messages = "Explain machine learning"
    model_name = "gemini-2.5-flash"
    allow_search = True

    response = get_response_from_ai_agents(model_name, system_prompt, messages, allow_search)
    print("AI Agent Response:", response)
