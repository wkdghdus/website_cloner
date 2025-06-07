import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

load_dotenv()


def LLM(temperature: float = 1, model: str = "gpt-4.1-mini",
        provider: str = os.environ.get("LLM_PROVIDER", "openai"), stream: bool = True) -> ChatAnthropic | ChatOpenAI:

    if provider == "openai":
        llm = ChatOpenAI(model=model, temperature=temperature, streaming=stream)
    elif provider == 'claude':
        llm = ChatAnthropic(model=model, temperature=temperature, streaming=stream)
    else:
        llm = ChatAnthropic(model=model, temperature=temperature, streaming=stream)

    return llm
