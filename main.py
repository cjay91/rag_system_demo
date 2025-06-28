from langsmith import utils
import os 
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from music_catalog.state_graph import music_catalog_subagent


load_dotenv()

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")  # Enables LangSmith tracing
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

import uuid

# Generate a unique thread ID for this conversation session
thread_id = uuid.uuid4()

# Define the user's question about music recommendations
question = "I like the Rolling Stones. What songs do you recommend by them or by other artists that I might like?"

# Set up configuration with the thread ID for maintaining conversation context
config = {"configurable": {"thread_id": thread_id}}

# Invoke the music catalog subagent with the user's question
# The agent will use its tools to search for Rolling Stones music and provide recommendations
result = music_catalog_subagent.invoke({"messages": [HumanMessage(content=question)]}, config=config)

# Display all messages from the conversation in a formatted way
for message in result["messages"]:
   message.pretty_print()