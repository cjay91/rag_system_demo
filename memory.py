from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore



# Initialize long-term memory store for persistent data between conversations
in_memory_store = InMemoryStore()

# Initialize checkpointer for short-term memory within a single thread/conversation
checkpointer = MemorySaver()

