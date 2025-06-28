from langgraph.prebuilt import ToolNode
from music_catalog.tools import get_albums_by_artist,get_songs_by_genre,get_tracks_by_artist,check_for_songs
from langchain_google_genai import ChatGoogleGenerativeAI  # Use LangChain wrapper
import os
# Create a list of all music-related tools for the agent
music_tools = [get_albums_by_artist, get_tracks_by_artist, get_songs_by_genre, check_for_songs]

llm = ChatGoogleGenerativeAI(model="gemma-3-4b-it",google_api_key=os.getenv("GEMINI_API_KEY"))

# Bind the music tools to the language model for use in the ReAct agent
llm_with_music_tools = llm.bind_tools(music_tools)

# Create a tool node that executes the music-related tools
# ToolNode is a pre-built LangGraph component that handles tool execution
music_tool_node = ToolNode(music_tools)

llm_with_music_tools,music_tool_node
