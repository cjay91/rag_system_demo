from langsmith import utils
import os 
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from music_catalog.state_graph import music_catalog_subagent
from invoice_info.tools import invoice_information_subagent
from nodes.Supervisor import supervisor_prebuilt
from state_graph import multi_agent_verify_graph

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")  # Enables LangSmith tracing
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

import uuid

# Generate a unique thread ID for this conversation session
# thread_id = uuid.uuid4()

# # Define the user's question about music recommendations
# question = "I like the Rolling Stones. What songs do you recommend by them or by other artists that I might like?"

# # Set up configuration with the thread ID for maintaining conversation context
# config = {"configurable": {"thread_id": thread_id}}

# # Invoke the music catalog subagent with the user's question
# # The agent will use its tools to search for Rolling Stones music and provide recommendations
# result = music_catalog_subagent.invoke({"messages": [HumanMessage(content=question)]}, config=config)

# # Display all messages from the conversation in a formatted way
# for message in result["messages"]:
#    message.pretty_print()

# Generate a unique thread ID for this conversation session
# thread_id = uuid.uuid4()

# # Define the user's question about their recent invoice and employee assistance
# question = "My customer id is 1. What was my most recent invoice, and who was the employee that helped me with it?"

# # Set up configuration with the thread ID for maintaining conversation context
# config = {"configurable": {"thread_id": thread_id}}

# # Invoke the invoice information subagent with the user's question
# # The agent will use its tools to search for invoice information and employee details
# result = invoice_information_subagent.invoke({"messages": [HumanMessage(content=question)]}, config=config)

# # Display all messages from the conversation in a formatted way
# for message in result["messages"]:
#     message.pretty_print()

# Generate a unique thread ID for this conversation session
# thread_id = uuid.uuid4()

# # Define a question that tests both invoice and music catalog capabilities
# question = "My customer ID is 1. How much was my most recent purchase? What albums do you have by U2?"

# # Set up configuration with the thread ID for maintaining conversation context
# config = {"configurable": {"thread_id": thread_id}}

# # Invoke the supervisor workflow with the multi-part question
# # The supervisor will route to appropriate subagents for invoice and music queries
# result = supervisor_prebuilt.invoke({"messages": [HumanMessage(content=question)]}, config=config)

# # Display all messages from the conversation in a formatted way
# for message in result["messages"]:
#     message.pretty_print()
from langgraph.types import Command


thread_id = uuid.uuid4()
question = "My phone number is +55 (12) 3923-5555."
config = {"configurable": {"thread_id": thread_id}}

# Initialize state with a messages list
initial_state = {"messages": [HumanMessage(content=question)]}
result = multi_agent_verify_graph.invoke(initial_state, config=config)
for message in result["messages"]:
    message.pretty_print()