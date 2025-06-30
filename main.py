from langsmith import utils
import os 
import uuid
from langgraph.types import Command
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from agents.Supervisor import supervisor_prebuilt
from state_graph import multi_agent_verify_graph

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
os.environ["LANGSMITH_TRACING"] = os.getenv("LANGSMITH_TRACING")  # Enables LangSmith tracing
os.environ["LANGSMITH_PROJECT"] = os.getenv("LANGSMITH_PROJECT")

thread_id = uuid.uuid4()
question = "My phone number is +55 (12) 3923-5555."
config = {"configurable": {"thread_id": thread_id}}

# Initialize state with a messages list
initial_state = {"messages": [HumanMessage(content=question)]}
result = multi_agent_verify_graph.invoke(initial_state, config=config)
for message in result["messages"]:
    message.pretty_print()