from langgraph.graph import StateGraph, START, END
from state import State
from music_catalog.music_assistant import music_assistant
from music_catalog.nodes import music_tool_node
from memory import checkpointer, in_memory_store
from langchain_core.runnables import RunnableConfig

def should_continue(state: State, config: RunnableConfig):
    """
    Conditional edge function that determines the next step in the ReAct agent workflow.
    
    This function examines the last message in the conversation to decide whether the agent
    should continue with tool execution or end the conversation.
    
    Args:
        state (State): Current state containing messages and other workflow data
        config (RunnableConfig): Configuration for the runnable execution
        
    Returns:
        str: Either "continue" to execute tools or "end" to finish the workflow
    """
    # Get all messages from the current state
    messages = state["messages"]
    
    # Examine the most recent message to check for tool calls
    last_message = messages[-1]
    
    # If the last message doesn't contain any tool calls, the agent is done
    if not last_message.tool_calls:
        return "end"
    # If there are tool calls present, continue to execute them
    else:
        return "continue"
    

# Create a new StateGraph instance for the music workflow
music_workflow = StateGraph(State)

# Add nodes to the graph
# music_assistant: The reasoning node that decides which tools to invoke or responds directly
music_workflow.add_node("music_assistant", music_assistant)
# music_tool_node: The execution node that handles all music-related tool calls
music_workflow.add_node("music_tool_node", music_tool_node)

# Add edges to define the flow of the graph
# Set the entry point - all queries start with the music assistant
music_workflow.add_edge(START, "music_assistant")

# Add conditional edge from music_assistant based on whether tools need to be called
music_workflow.add_conditional_edges(
    "music_assistant",
    # Conditional function that determines the next step
    should_continue,
    {
        # If tools need to be executed, route to tool node
        "continue": "music_tool_node",
        # If no tools needed, end the workflow
        "end": END,
    },
)

# After tool execution, always return to the music assistant for further processing
music_workflow.add_edge("music_tool_node", "music_assistant")

# Compile the graph with checkpointer for short-term memory and store for long-term memory
music_catalog_subagent = music_workflow.compile(
    name="music_catalog_subagent", 
    checkpointer=checkpointer, 
    store=in_memory_store
)

# Display the compiled graph structure
print(music_catalog_subagent.get_graph().draw_ascii())

