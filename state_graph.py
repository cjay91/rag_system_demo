from langgraph.graph import StateGraph, START, END
from core.state import State
from core.memory import checkpointer, in_memory_store
from langchain_core.runnables import RunnableConfig
from nodes.human_input import human_input, verify_info, should_interrupt
from nodes.Supervisor import supervisor_prebuilt
from langchain_core.messages import ToolMessage, SystemMessage, HumanMessage
from database.db import get_database

# Create a new StateGraph instance for the multi-agent workflow with verification
multi_agent_verify = StateGraph(State)

# Add new nodes for customer verification and human interaction
multi_agent_verify.add_node("verify_info", verify_info)
multi_agent_verify.add_node("human_input", human_input)
# Add the existing supervisor agent as a node
multi_agent_verify.add_node("supervisor", supervisor_prebuilt)

# Define the graph's entry point: always start with information verification
multi_agent_verify.add_edge(START, "verify_info")

# Add a conditional edge from verify_info to decide whether to continue or interrupt
multi_agent_verify.add_conditional_edges(
    "verify_info",
    should_interrupt, # The function that checks if customer_id is verified
    {
        "continue": "supervisor", # If verified, proceed to the supervisor
        "interrupt": "human_input", # If not verified, interrupt for human input
    },
)
# After human input, always loop back to verify_info to re-attempt verification
multi_agent_verify.add_edge("human_input", "verify_info")
# After the supervisor completes its task, the workflow ends
multi_agent_verify.add_edge("supervisor", END)

# Compile the complete graph with checkpointer and long-term memory store
multi_agent_verify_graph = multi_agent_verify.compile(
    name="multi_agent_verify", 
    checkpointer=checkpointer, 
    store=in_memory_store
)

# Display the updated graph structure
print(multi_agent_verify_graph.get_graph().draw_ascii())
