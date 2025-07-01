import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()


def llm_provider():
    return ChatOpenAI(
        model="gpt-3.5-turbo",  # or "gpt-4o", etc.
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )