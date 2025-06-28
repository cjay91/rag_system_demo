from typing_extensions import TypedDict
from typing import Annotated, List
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.managed.is_last_step import RemainingSteps

class State(TypedDict):
    """
    State schema for the multi-agent customer support workflow.
    
    This defines the shared data structure that flows between nodes in the graph,
    representing the current snapshot of the conversation and agent state.
    """
    # Customer identifier retrieved from account verification
    customer_id: str
    
    # Conversation history with automatic message aggregation
    messages: Annotated[list[AnyMessage], add_messages]
    
    # User preferences and context loaded from long-term memory store
    loaded_memory: str
    
    # Counter to prevent infinite recursion in agent workflow
    remaining_steps: RemainingSteps 